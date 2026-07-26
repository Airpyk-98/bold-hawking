import os
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapter_files = [f"chapter_{str(i).zfill(2)}.html" for i in range(1, 8)]

all_chapters_data = []

def extract_references_from_chapter(ch_file):
    path = os.path.join(base_dir, ch_file)
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    h1 = soup.find('h1')
    chapter_title = h1.get_text().strip() if h1 else ""
    
    # Locate References heading element
    ref_heading_el = None
    for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong', 'span']):
        txt = el.get_text().strip()
        if re.search(r'^\s*references\s*$', txt, re.IGNORECASE):
            ref_heading_el = el
            break
            
    if not ref_heading_el:
        for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong', 'span']):
            if 'references' in el.get_text().lower() and len(el.get_text().strip()) < 30:
                ref_heading_el = el
                break

    extracted_refs = []

    if ch_file == "chapter_05.html":
        # In chapter 05, references are in p/div elements or text after 'References' heading
        # Find all siblings or elements after ref_heading_el
        # Let's inspect all text blocks that start with numbers "1.", "2.", etc.
        # Or parse the div containing the references
        ref_container = None
        if ref_heading_el:
            parent = ref_heading_el.parent
            while parent and parent.name not in ['div', 'section', 'body']:
                parent = parent.parent
            ref_container = parent
            
        if not ref_container:
            ref_container = soup
            
        # Find text blocks starting with number followed by dot, e.g. "1. Alonso, J..."
        # Let's find all tags containing reference text
        paras = ref_container.find_all(['p', 'div', 'li'])
        for p in paras:
            p_text = p.get_text(separator=" ", strip=True)
            match = re.match(r'^(\d+)\.\s+(.*)$', p_text)
            if match and int(match.group(1)) <= 25:
                # Make sure it's a reference (has author/year or publication)
                ref_num = int(match.group(1))
                # avoid duplicate refs
                if not any(r['ref_num'] == ref_num for r in extracted_refs):
                    extracted_refs.append({
                        "ref_num": ref_num,
                        "raw_html": str(p).strip(),
                        "text": p_text,
                        "tag": p.name
                    })
    else:
        # For other chapters, check <ol> tags first
        ols = soup.find_all('ol')
        if ols:
            # Main reference ol is usually the last ol or the one after ref_heading_el
            ref_ol = None
            if ref_heading_el:
                next_ol = ref_heading_el.find_next('ol')
                if next_ol:
                    ref_ol = next_ol
            if not ref_ol:
                ref_ol = ols[-1]
                
            lis = ref_ol.find_all('li', recursive=False)
            if not lis:
                lis = ref_ol.find_all('li')
                
            for idx, li in enumerate(lis, 1):
                extracted_refs.append({
                    "ref_num": idx,
                    "raw_html": str(li).strip(),
                    "text": li.get_text(separator=" ", strip=True),
                    "tag": li.name
                })
        else:
            # Fallback for non-ol references
            pass
            
    # Process each reference detail
    detailed_refs = []
    for ref in extracted_refs:
        raw_html = ref["raw_html"]
        text = ref["text"]
        
        # Analyze Anchors
        a_soup = BeautifulSoup(raw_html, 'html.parser')
        anchors = a_soup.find_all('a')
        a_details = []
        for a in anchors:
            a_details.append({
                "href": a.get('href', ''),
                "text": a.get_text().strip(),
                "raw_a": str(a).strip()
            })
            
        # Nested <a> detection
        has_nested_a = False
        if raw_html.count('<a ') > 1 and ('</a>\n</a>' in raw_html or '</a></span></a>' in raw_html or '</a></a>' in raw_html or any(a.find('a') for a in anchors)):
            has_nested_a = True
            
        # Regex for DOIs
        doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+'
        text_dois = [re.sub(r'[\.,;\)]+$', '', d) for d in re.findall(doi_pattern, text)]
        html_dois = [re.sub(r'[\.,;\)]+$', '', d) for d in re.findall(doi_pattern, raw_html)]
        all_dois = list(set(text_dois + html_dois))
        
        # Plain text DOIs (not in href)
        hrefs = " ".join([a["href"] for a in a_details])
        plain_dois = [d for d in all_dois if d not in hrefs]
        
        # Extract URLs
        url_pattern = r'https?://[^\s<">]+'
        all_urls = list(set([u.rstrip('.,;)') for u in re.findall(url_pattern, text + " " + raw_html)]))
        
        # Author, Year, Title extraction
        # Pattern 1: Author, A. A. (Year). Title. Journal...
        # Pattern 2: 1. Author, A. A. (Year). Title...
        clean_text = re.sub(r'^\d+\.\s*', '', text)
        apa_match = re.match(r'^([^\(\n]+)\s*\((19\d\d|20\d\d)[a-z]?\)\.\s*([^\.]+)\.', clean_text)
        
        authors = apa_match.group(1).strip() if apa_match else "Unparsed/Non-standard"
        year = apa_match.group(2).strip() if apa_match else "Unparsed/Non-standard"
        title = apa_match.group(3).strip() if apa_match else clean_text[:80]
        
        detailed_refs.append({
            "ref_num": ref["ref_num"],
            "authors": authors,
            "year": year,
            "title": title,
            "full_text": text,
            "raw_html": raw_html,
            "anchor_count": len(anchors),
            "anchors": a_details,
            "has_nested_a": has_nested_a,
            "all_dois": all_dois,
            "plain_dois": plain_dois,
            "all_urls": all_urls
        })
        
    return {
        "file": ch_file,
        "title": chapter_title,
        "ref_count": len(detailed_refs),
        "ref_heading_found": ref_heading_el is not None,
        "heading_tag": ref_heading_el.name if ref_heading_el else None,
        "references": detailed_refs
    }

chapters_data = [extract_references_from_chapter(ch) for ch in chapter_files]

out_json = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_1\inventory_ch1_7.json"
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(chapters_data, f, indent=2, ensure_ascii=False)

print(f"Full inventory written to {out_json}")
