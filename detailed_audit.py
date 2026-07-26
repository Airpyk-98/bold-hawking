import os
import sys
import re
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def parse_item(elem, chap_num, ref_num):
    raw_html = str(elem)
    text = elem.get_text().strip()
    
    # Check nested <a>
    nested_a = False
    for a in elem.find_all('a'):
        if a.find('a'):
            nested_a = True
            break
            
    # Find all doi hrefs or plain text DOIs
    doi_matches = re.findall(r'10\.\d{4,9}/[^\s"<>\)]+', raw_html)
    cleaned_dois = []
    for d in doi_matches:
        d = d.rstrip('.\'")>]')
        if d not in cleaned_dois:
            cleaned_dois.append(d)
            
    # Find hrefs in <a> tags
    hrefs = [a['href'] for a in elem.find_all('a') if a.has_attr('href')]
    
    return {
        'chapter': chap_num,
        'ref_num': ref_num,
        'tag_name': elem.name,
        'text': text,
        'raw_html': raw_html,
        'has_nested_a': nested_a,
        'extracted_dois': cleaned_dois,
        'hrefs': hrefs
    }

def extract_references_from_chapter(chap_num):
    filepath = f"chapters/chapter_{chap_num:02d}.html"
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    if chap_num == 1:
        ols = soup.find_all('ol')
        if ols:
            for idx, item in enumerate(ols[0].find_all('li', recursive=False)):
                results.append(parse_item(item, chap_num, idx+1))
    elif chap_num == 2:
        ols = soup.find_all('ol')
        ref_ol = None
        for ol in ols:
            items = ol.find_all('li', recursive=False)
            if len(items) == 18:
                ref_ol = ol
                break
        if ref_ol:
            for idx, item in enumerate(ref_ol.find_all('li', recursive=False)):
                results.append(parse_item(item, chap_num, idx+1))
    elif chap_num == 3:
        ols = soup.find_all('ol')
        if ols:
            for idx, item in enumerate(ols[0].find_all('li', recursive=False)):
                results.append(parse_item(item, chap_num, idx+1))
    elif chap_num == 4:
        pass
    elif chap_num == 5:
        # Chapter 5: Find the references heading or paragraph block
        # In chapter_05.html, let's see how paragraphs are structured
        ref_h = None
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p']):
            if 'reference' in h.get_text().lower():
                ref_h = h
                break
        if ref_h:
            curr = ref_h.find_next_sibling()
            idx = 1
            while curr:
                text = curr.get_text().strip()
                if text and curr.name == 'p':
                    results.append(parse_item(curr, chap_num, idx))
                    idx += 1
                curr = curr.find_next_sibling()
        else:
            idx = 1
            for p in soup.find_all('p'):
                text = p.get_text().strip()
                if re.match(r'^\d+[\.\)]\s*', text):
                    results.append(parse_item(p, chap_num, idx))
                    idx += 1
    elif chap_num == 6:
        ols = soup.find_all('ol')
        ref_ol = None
        for ol in ols:
            items = ol.find_all('li', recursive=False)
            if len(items) == 9:
                ref_ol = ol
                break
        if not ref_ol and ols:
            ref_ol = ols[-1]
        if ref_ol:
            for idx, item in enumerate(ref_ol.find_all('li', recursive=False)):
                results.append(parse_item(item, chap_num, idx+1))
    elif chap_num == 7:
        ols = soup.find_all('ol')
        ref_ol = None
        for ol in ols:
            items = ol.find_all('li', recursive=False)
            if len(items) == 14:
                ref_ol = ol
                break
        if not ref_ol and ols:
            ref_ol = ols[-1]
        if ref_ol:
            for idx, item in enumerate(ref_ol.find_all('li', recursive=False)):
                results.append(parse_item(item, chap_num, idx+1))
                
    return results

all_refs = []
for c in range(1, 8):
    refs = extract_references_from_chapter(c)
    print(f"Chapter {c}: extracted {len(refs)} references.")
    all_refs.extend(refs)

print(f"\nTotal extracted references across Ch 1-7: {len(all_refs)}")
print(f"Nested <a> count: {sum(1 for r in all_refs if r['has_nested_a'])}")

with open('extracted_refs_ch1_7.json', 'w', encoding='utf-8') as f:
    json.dump(all_refs, f, indent=2, ensure_ascii=False)
