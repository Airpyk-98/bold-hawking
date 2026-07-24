import os
import re
import urllib.request
import urllib.error
import json
from bs4 import BeautifulSoup

chapters = [
    f"chapter_{i}.html" for i in range(42, 51)
]
base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

reports = []

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlopen(req, timeout=5)
        return "OK"
    except urllib.error.HTTPError as e:
        if e.code in [403, 405]:
            return "BOT_BLOCK"
        return f"HTTP_ERROR_{e.code}"
    except Exception as e:
        return f"ERROR_{str(e)}"

for ch in chapters:
    path = os.path.join(base_dir, ch)
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    # Find heading that contains 'References'
    ref_heading = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong', 'span'] and tag.get_text() and 'References' in tag.get_text().strip())
    
    if not ref_heading:
        reports.append(f"Chapter {ch}: No References heading found.")
        continue
        
    # Find the container or next siblings
    # Often it might be a <p> with <strong>References</strong>
    
    # We want to check if the references are in an <ol>
    # Let's find all <ol> tags after the heading
    
    # If the heading is a <p> or <span> etc, we need to look at next siblings
    parent = ref_heading.parent
    if ref_heading.name in ['strong', 'span']:
        # sometimes it's <p><span style="color: #339966"><strong>References</strong></span></p>
        ref_heading = ref_heading.find_parent('p') or ref_heading
        
    siblings = ref_heading.find_next_siblings()
    
    # Check if there is an <ol> among siblings
    ol_tag = None
    p_refs = []
    
    for sib in siblings:
        if sib.name == 'ol':
            ol_tag = sib
            break
        elif sib.name == 'p' and sib.get_text().strip() and re.match(r'^\d+\.', sib.get_text().strip()):
            p_refs.append(sib)
            
    if not ol_tag and p_refs:
        reports.append(f"Chapter {ch}: References are in <p> tags instead of <ol>. Found {len(p_refs)} references.")
        for p in p_refs:
            text = p.get_text().strip()
            if 'http' in text or '10.' in text:
                reports.append(f"  - Ref: {text[:50]}...")
        # Check them anyway
        items_to_check = p_refs
    elif ol_tag:
        items_to_check = ol_tag.find_all('li', recursive=False)
    else:
        reports.append(f"Chapter {ch}: No references found after heading.")
        continue
        
    for item in items_to_check:
        html_str = str(item)
        text = item.get_text().strip()
        
        # Check for plain text links
        # If text contains 'http' or '10.' but it's not wrapped in <a>
        links = item.find_all('a')
        hrefs = [a.get('href') for a in links if a.get('href')]
        
        # Also check if text has "10.xxxx" but no hrefs have it
        doi_match = re.search(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', text, re.IGNORECASE)
        url_match = re.search(r'https?://[^\s]+', text)
        
        has_plain_text_doi = False
        has_plain_text_url = False
        
        if doi_match:
            doi_str = doi_match.group(0).rstrip('.')
            # is it in any href?
            in_href = any(doi_str in h for h in hrefs)
            if not in_href:
                reports.append(f"Chapter {ch}: Plain text DOI found: {doi_str}")
                reports.append(f"  - Ref: {text}")
                
        if url_match:
            url_str = url_match.group(0).rstrip('.')
            # check if it's the text content of a link, but wait, the check is if it's not in an <a> tag
            # BS4 item.find_all(text=re.compile('http')) might be better, but let's just check if there's any <a> tag wrapping it.
            # Actually, plain text URL means there is a URL in the text that doesn't correspond to an <a> tag.
            pass
            
        for a in links:
            href = a.get('href')
            if not href: continue
            
            if 'doi.org' in href:
                if not href.startswith('https://doi.org/'):
                    reports.append(f"Chapter {ch}: Malformed DOI link (must start with https://doi.org/): {href}")
                else:
                    # check if resolvable
                    status = check_url(href)
                    if status not in ["OK", "BOT_BLOCK"]:
                        reports.append(f"Chapter {ch}: Broken DOI link ({status}): {href}")
            elif '10.' in href and 'doi' not in href:
                reports.append(f"Chapter {ch}: Link might be a plain DOI without https://doi.org/: {href}")
            else:
                # Normal url
                status = check_url(href)
                if status not in ["OK", "BOT_BLOCK"]:
                    reports.append(f"Chapter {ch}: Broken URL ({status}): {href}")

with open('audit_report.txt', 'w', encoding='utf-8') as f:
    for r in reports:
        f.write(r + '\n')

print("Audit script finished.")
