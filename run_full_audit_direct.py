import os
import sys
import re
import json
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
EXTRACTED_FILE = os.path.join(BASE_DIR, 'extracted_refs_ch1_7.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'full_doi_audit.json')

def string_similarity(a, b):
    a_clean = re.sub(r'[^\w\s]', '', a.lower()).strip()
    b_clean = re.sub(r'[^\w\s]', '', b.lower()).strip()
    return SequenceMatcher(None, a_clean, b_clean).ratio()

def check_doi_crossref_api(doi):
    if not doi:
        return 404, None, None
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
    doi_clean = doi_clean.rstrip('.\'")>]')
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                msg = data.get('message', {})
                titles = msg.get('title', [])
                title = titles[0] if titles else ""
                return 200, title, msg.get('DOI')
    except urllib.error.HTTPError as e:
        return e.code, None, None
    except Exception as e:
        return str(e), None, None
    return 404, None, None

def query_crossref_search(text):
    cleaned = re.sub(r'https?://\S+', '', text)
    cleaned = re.sub(r'10\.\d{4,9}/\S+', '', cleaned)
    cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned).strip()
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(cleaned[:250])}&rows=3"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                cand_doi = item.get('DOI')
                cand_titles = item.get('title', [])
                cand_title = cand_titles[0] if cand_titles else ""
                score = string_similarity(cleaned, cand_title)
                results.append({
                    'doi': cand_doi,
                    'title': cand_title,
                    'score': score
                })
            return results
    except Exception as e:
        return []

with open(EXTRACTED_FILE, 'r', encoding='utf-8') as f:
    refs = json.load(f)

results = []

for idx, r in enumerate(refs):
    ch = r['chapter']
    rnum = r['ref_num']
    text = r['text']
    dois = r['extracted_dois']
    
    doi = dois[0] if dois else None
    status, title, valid_doi = check_doi_crossref_api(doi) if doi else (None, None, None)
    
    cand = None
    if status != 200:
        search_res = query_crossref_search(text)
        if search_res:
            cand = search_res[0]
            
    print(f"Ch{ch} Ref{rnum:02d}: Existing DOI='{doi}' -> Status={status}")
    if status == 200:
        print(f"   [VALID] Verified CrossRef Title: {title[:70]}")
    elif cand:
        print(f"   [SEARCH] Candidate DOI='{cand['doi']}' (score {cand['score']:.2f}) -> {cand['title'][:70]}")
    else:
        print(f"   [NO MATCH] No DOI found.")
        
    results.append({
        'chapter': ch,
        'ref_num': rnum,
        'text': text,
        'existing_doi': doi,
        'status': status,
        'verified_title': title,
        'candidate': cand,
        'raw_html': r['raw_html'],
        'has_nested_a': r['has_nested_a']
    })

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nSaved to {OUTPUT_FILE}")
