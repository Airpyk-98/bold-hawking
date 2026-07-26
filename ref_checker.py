import os
import sys
import re
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding='utf-8')

with open('extracted_refs_ch1_7.json', 'r', encoding='utf-8') as f:
    refs = json.load(f)

def string_similarity(a, b):
    a_clean = re.sub(r'[^\w\s]', '', a.lower()).strip()
    b_clean = re.sub(r'[^\w\s]', '', b.lower()).strip()
    return SequenceMatcher(None, a_clean, b_clean).ratio()

def check_doi_http(doi):
    url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e), None

def query_crossref(text):
    # Extract title candidates or search text
    # Remove DOIs and URLs
    cleaned = re.sub(r'https?://\S+', '', text)
    cleaned = re.sub(r'10\.\d{4,9}/\S+', '', cleaned)
    cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned).strip()
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(cleaned[:250])}&rows=3"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                candidate_doi = item.get('DOI')
                candidate_titles = item.get('title', [])
                cand_title = candidate_titles[0] if candidate_titles else ""
                # Calculate similarity with text or title
                score = string_similarity(cleaned, cand_title)
                results.append({
                    'doi': candidate_doi,
                    'title': cand_title,
                    'score': score
                })
            return results
    except Exception as e:
        print(f"CrossRef error: {e}")
        return []

audited_refs = []

for idx, ref in enumerate(refs):
    ch = ref['chapter']
    rnum = ref['ref_num']
    text = ref['text']
    dois = ref['extracted_dois']
    hrefs = ref['hrefs']
    nested = ref['has_nested_a']
    
    print(f"[{idx+1}/{len(refs)}] Auditing Ch {ch} Ref {rnum}...")
    
    existing_doi = dois[0] if dois else None
    existing_status = None
    if existing_doi:
        status, target_url = check_doi_http(existing_doi)
        existing_status = status
        print(f"  Existing DOI: {existing_doi} -> {existing_status}")
    else:
        print("  No existing DOI found.")
        
    crossref_matches = []
    # If existing DOI is 404 or missing, or to verify strict title match
    if not existing_doi or existing_status == 404 or isinstance(existing_status, str):
        crossref_matches = query_crossref(text)
        if crossref_matches:
            top = crossref_matches[0]
            print(f"  Top CrossRef Match: {top['doi']} (score: {top['score']:.2f}) -> Title: {top['title'][:60]}")
            
    audited_refs.append({
        'chapter': ch,
        'ref_num': rnum,
        'text': text,
        'has_nested_a': nested,
        'existing_dois': dois,
        'existing_status': existing_status,
        'crossref_matches': crossref_matches,
        'raw_html': ref['raw_html']
    })
    time.sleep(0.2)

with open('audited_refs_ch1_7.json', 'w', encoding='utf-8') as f:
    json.dump(audited_refs, f, indent=2, ensure_ascii=False)

print("\nAudit completed and saved to audited_refs_ch1_7.json")
