import os
import json
import re
from bs4 import BeautifulSoup

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapter_files = [f"chapter_{str(i).zfill(2)}.html" for i in range(1, 8)]

local_results = []

for ch_file in chapter_files:
    path = os.path.join(base_dir, ch_file)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Title / Header
    h1 = soup.find('h1')
    title = h1.get_text().strip() if h1 else "No H1"
    
    # 2. Reference section search
    # Find heading or div with text References
    ref_headings = []
    for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong']):
        txt = el.get_text().strip()
        if re.search(r'^\s*references\s*$', txt, re.IGNORECASE) or re.search(r'^\s*\d+\.?\d*\s+references\s*$', txt, re.IGNORECASE) or 'references' in txt.lower():
            ref_headings.append({
                "tag": el.name,
                "text": txt,
                "class": el.get('class')
            })
            
    ols = soup.find_all('ol')
    uls = soup.find_all('ul')
    
    # Analyze all OLs and LIs in document
    ol_details = []
    for ol_idx, ol in enumerate(ols, 1):
        lis = ol.find_all('li')
        ol_details.append({
            "ol_index": ol_idx,
            "li_count": len(lis),
            "parent_tag": ol.parent.name if ol.parent else None,
            "prev_sibling": str(ol.previous_sibling).strip()[:100] if ol.previous_sibling else None
        })
    
    # Select the references OL
    ref_ol = ols[-1] if ols else None
    
    references_list = []
    if ref_ol:
        lis = ref_ol.find_all('li', recursive=False)
        if not lis:
            lis = ref_ol.find_all('li')
            
        for idx, li in enumerate(lis, 1):
            raw_html = str(li).strip()
            text = li.get_text(separator=" ", strip=True)
            
            # Anchor tag analysis
            a_tags = li.find_all('a')
            a_list = []
            for a in a_tags:
                a_list.append({
                    "href": a.get('href', ''),
                    "text": a.get_text().strip(),
                    "raw_a": str(a).strip()
                })
            
            # Check for double / nested <a> tags
            has_nested_a = False
            if raw_html.count('<a ') > 1 and '</a>\n</a>' in raw_html or '</a></span></a>' in raw_html or '</a></a>' in raw_html or (a_tags and any(a.find('a') for a in a_tags)):
                has_nested_a = True
                
            # Extract plain DOIs
            dois_in_text = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
            dois_in_text = [re.sub(r'[\.,;\)]+$', '', d) for d in dois_in_text]
            
            # Extract plain DOIs from html
            dois_in_html = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', raw_html)
            dois_in_html = [re.sub(r'[\.,;\)]+$', '', d) for d in dois_in_html]
            
            all_dois = list(set(dois_in_text + dois_in_html))
            
            # Check if any DOI in reference is plain text (not wrapped in <a href="https://doi.org/...">)
            plain_dois = []
            for d in all_dois:
                # check if d is in any href
                in_href = any(d in a['href'] for a in a_list)
                if not in_href:
                    plain_dois.append(d)
            
            # Check formatting anomalies
            # Author, Year, Title, Journal
            # Standard APA match: Author (Year). Title. Journal...
            author_year_match = re.match(r'^([^(\n]+)\s*\((19\d\d|20\d\d)[a-z]?\)\.\s*(.+)$', text)
            
            references_list.append({
                "ref_num": idx,
                "text": text,
                "raw_html": raw_html,
                "a_tags": a_list,
                "a_count": len(a_tags),
                "has_nested_a": has_nested_a,
                "all_dois": all_dois,
                "plain_dois": plain_dois,
                "apa_structured": author_year_match is not None,
                "author_part": author_year_match.group(1).strip() if author_year_match else None,
                "year_part": author_year_match.group(2).strip() if author_year_match else None,
                "title_rest": author_year_match.group(3).strip() if author_year_match else None
            })
            
    local_results.append({
        "file": ch_file,
        "h1_title": title,
        "ref_headings": ref_headings,
        "ol_summary": ol_details,
        "ref_count": len(references_list),
        "references": references_list
    })

out_json = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_1\local_analysis.json"
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(local_results, f, indent=2, ensure_ascii=False)

print(f"Local analysis saved to {out_json}")
