import os
import sys
import re
import json
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

def verify_doi_crossref(doi):
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
    doi_clean = doi_clean.rstrip('.\'")>]')
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                title = data.get('message', {}).get('title', [''])[0]
                return 200, title
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e), None
    return 404, None

def verify_chapter(chap_num):
    filepath = os.path.join(BASE_DIR, f"chapter_{chap_num:02d}.html")
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    print(f"\n=================== CHAPTER {chap_num:02d} VERIFICATION ===================")
    
    # Check nested <a>
    nested_a_count = 0
    for a in soup.find_all('a'):
        if a.find('a'):
            nested_a_count += 1
    print(f"Nested <a> tags in entire chapter: {nested_a_count}")
    
    ols = soup.find_all('ol')
    print(f"Total <ol> elements: {len(ols)}")
    
    ref_ol = None
    expected_counts = {1: 4, 2: 18, 3: 19, 5: 20, 6: 9, 7: 14}
    
    if chap_num == 4:
        print("Chapter 4: No reference list (Introductory chapter).")
        return
        
    target_count = expected_counts.get(chap_num)
    for ol in ols:
        items = ol.find_all('li', recursive=False)
        if len(items) == target_count:
            ref_ol = ol
            break
            
    if not ref_ol and ols:
        ref_ol = ols[-1]
        
    if not ref_ol:
        print(f"ERROR: Reference <ol> not found for Chapter {chap_num}!")
        return
        
    items = ref_ol.find_all('li', recursive=False)
    print(f"Reference <ol> found with {len(items)} items.")
    
    doi_count = 0
    valid_doi_count = 0
    broken_doi_count = 0
    
    for idx, li in enumerate(items, 1):
        links = li.find_all('a')
        doi_links = [a for a in links if 'doi.org' in a.get('href', '') or a.get('href', '').startswith('10.')]
        
        if doi_links:
            doi_count += 1
            for a in doi_links:
                href = a['href']
                status, title = verify_doi_crossref(href)
                if status == 200:
                    valid_doi_count += 1
                    print(f"  [Ref {idx:02d}] 200 OK | {href} | Title: {title[:60]}")
                else:
                    broken_doi_count += 1
                    print(f"  [Ref {idx:02d}] FAIL ({status}) | {href}")
        else:
            print(f"  [Ref {idx:02d}] No DOI link (Book/Website/TK)")
            
    print(f"Chapter {chap_num} Summary: Total Refs={len(items)}, DOIs={doi_count}, Verified 200 OK DOIs={valid_doi_count}, Broken DOIs={broken_doi_count}")

for c in range(1, 8):
    verify_chapter(c)
