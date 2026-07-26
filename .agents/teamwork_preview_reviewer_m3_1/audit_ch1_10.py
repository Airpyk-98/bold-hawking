import os
import re
import urllib.request
import urllib.error
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

CHAPTERS_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
TARGET_CHAPTERS = [f"chapter_{i:02d}.html" for i in range(1, 11)]

def check_nested_anchors(html_content, filename):
    soup = BeautifulSoup(html_content, 'html.parser')
    nested_found = []
    
    # 1. DOM hierarchy check
    for a in soup.find_all('a'):
        inner_a = a.find_all('a')
        if inner_a:
            nested_found.append((str(a), [str(i) for i in inner_a]))
            
    # 2. Regex check for raw string nested anchors
    raw_matches = re.findall(r'<a\s+[^>]*>\s*<a\s+[^>]*>', html_content, re.IGNORECASE)
    
    return nested_found, raw_matches

def check_references_structure(html_content, filename):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for reference section header
    ref_headers = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'span', 'strong']):
        if tag.get_text() and 'reference' in tag.get_text().strip().lower():
            # Filter out casual mentions, look for headings/section titles
            text = tag.get_text().strip()
            if text.lower() in ['references', 'reference', 'references:'] or tag.name in ['h1', 'h2', 'h3', 'h4']:
                ref_headers.append(tag)
                
    results = {
        'headers': [h.get_text().strip() for h in ref_headers],
        'ol_count': 0,
        'li_count': 0,
        'raw_p_refs': [],
        'structure_status': 'UNKNOWN'
    }
    
    # Find all <ol> in references area or overall
    ol_tags = soup.find_all('ol')
    results['ol_count'] = len(ol_tags)
    
    total_li = sum(len(ol.find_all('li')) for ol in ol_tags)
    results['li_count'] = total_li
    
    # Check if there are raw paragraphs starting with numbers under references section
    # e.g. <p>1. Author...</p> or <p>[1] Author...</p>
    p_tags = soup.find_all('p')
    for p in p_tags:
        text = p.get_text().strip()
        if re.match(r'^\s*(\[\d+\]|\d+\.)\s+[A-Z]', text):
            results['raw_p_refs'].append(text[:60])
            
    if filename == "chapter_04.html":
        # Chapter 4 might have no references as noted by worker
        if len(ol_tags) == 0 and total_li == 0:
            results['structure_status'] = 'NO_REFERENCES_PRESENT'
        else:
            results['structure_status'] = 'OL_LI_PRESENT'
    else:
        if total_li > 0 and len(results['raw_p_refs']) == 0:
            results['structure_status'] = 'OL_LI_STRUCTURED'
        elif total_li > 0 and len(results['raw_p_refs']) > 0:
            results['structure_status'] = 'MIXED_STRUCTURE'
        else:
            results['structure_status'] = 'NO_OL_FOUND'
            
    return results

def check_doi_formatting_and_links(html_content, filename):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    doi_anchors = []
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text()
        if 'doi.org' in href or '10.' in href:
            doi_anchors.append({'href': href, 'text': text, 'outer': str(a)})
            
    # Check for un-anchored raw DOIs in text
    # Exclude inside <a ...> tags
    text_content = str(soup)
    # pattern to find 10.xxxx/yyyy not inside href="..."
    raw_dois = re.findall(r'(?<!href=")(?<!href=\')(?:https?://doi\.org/)?10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text_content)
    
    # Filter out ones that are actually part of anchor tags
    unanchored_dois = []
    for rd in raw_dois:
        # check if it's enclosed in <a ...> ... </a>
        # simple check: if rd appears in an anchor href or anchor text, it's anchored
        anchored = False
        for da in doi_anchors:
            if rd in da['href'] or rd in da['text'] or rd in da['outer']:
                anchored = True
                break
        if not anchored:
            unanchored_dois.append(rd)
            
    return doi_anchors, unanchored_dois

def test_doi_url(url):
    # Standardize url
    if not url.startswith('http'):
        url = 'https://doi.org/' + url
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        # Use no-redirect opener to check 302/200 handle resolution without WAF block
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = urllib.request.build_opener(NoRedirectHandler)
        resp = opener.open(req, timeout=10)
        return resp.status, "OK"
    except urllib.error.HTTPError as e:
        if e.code in [301, 302, 303, 307, 308]:
            return e.code, "Redirect OK"
        return e.code, str(e.reason)
    except Exception as e:
        return 0, str(e)

def get_crossref_metadata(doi_clean):
    url = f"https://api.crossref.org/works/{doi_clean}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; mailto:reviewer@example.com)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            title = data.get('message', {}).get('title', [''])[0]
            container = data.get('message', {}).get('container-title', [''])[0]
            return title, container
    except Exception as e:
        return None, str(e)

def main():
    print("=== STARTING AUDIT FOR CHAPTERS 1-10 ===")
    
    total_nested = 0
    total_dois = 0
    doi_status_counts = {'200/302': 0, 'FAIL': 0}
    all_doi_details = []

    for filename in TARGET_CHAPTERS:
        filepath = os.path.join(CHAPTERS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[-] FILE NOT FOUND: {filepath}")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        nested_dom, nested_regex = check_nested_anchors(content, filename)
        ref_struct = check_references_structure(content, filename)
        doi_anchors, unanchored_dois = check_doi_formatting_and_links(content, filename)
        
        num_nested = len(nested_dom) + len(nested_regex)
        total_nested += num_nested
        total_dois += len(doi_anchors)
        
        print(f"\n--- {filename} ---")
        print(f"Nested Anchors: {num_nested}")
        print(f"Ref Structure Status: {ref_struct['structure_status']} (OL tags: {ref_struct['ol_count']}, LI tags: {ref_struct['li_count']})")
        print(f"DOI Anchors Count: {len(doi_anchors)}")
        print(f"Unanchored DOIs Count: {len(unanchored_dois)}")
        
        if num_nested > 0:
            print(f"  [!] DOM Nested: {nested_dom}")
            print(f"  [!] Regex Nested: {nested_regex}")
            
        if unanchored_dois:
            print(f"  [!] Unanchored DOIs: {unanchored_dois}")
            
        # Collect DOI links for testing
        for da in doi_anchors:
            all_doi_details.append({
                'chapter': filename,
                'href': da['href'],
                'text': da['text'],
                'outer': da['outer']
            })

    print(f"\n==========================================")
    print(f"Total Chapters Audited: 10")
    print(f"Total Nested Anchors Found: {total_nested}")
    print(f"Total DOI Anchors Found: {total_dois}")
    print(f"==========================================\n")
    
    # Write details to report file
    with open("audit_ch1_10_results.json", "w", encoding="utf-8") as f:
        json.dump(all_doi_details, f, indent=2)

if __name__ == '__main__':
    main()
