import os
import re
import json
import urllib.request
import urllib.parse
import difflib
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
headers = {'User-Agent': 'mailto:worker_m2_2@example.com'}

workspace_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
chapters_dir = os.path.join(workspace_dir, "chapters")

def clean_text(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def title_similarity(t1, t2):
    t1_clean = re.sub(r'[^a-zA-Z0-9 ]', '', t1.lower()).strip()
    t2_clean = re.sub(r'[^a-zA-Z0-9 ]', '', t2.lower()).strip()
    words1 = set(w for w in t1_clean.split() if len(w) > 3)
    words2 = set(w for w in t2_clean.split() if len(w) > 3)
    if not words1 or not words2:
        return 0.0
    intersection = words1.intersection(words2)
    ratio = difflib.SequenceMatcher(None, t1_clean, t2_clean).ratio()
    overlap_ratio = len(intersection) / max(len(words1), len(words2))
    return max(ratio, overlap_ratio)

def check_doi_crossref(doi):
    clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi).strip().rstrip('.,;)')
    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            msg = data.get('message', {})
            title = msg.get('title', [''])[0]
            return {'valid': True, 'title': title, 'clean_doi': clean_doi}
    except Exception as e:
        return {'valid': False, 'error': str(e), 'clean_doi': clean_doi}

def search_crossref(ref_text):
    # Remove index numbers, URLs, DOIs from search string
    clean_search = re.sub(r'^\d+[\.\)]\s*', '', ref_text)
    clean_search = re.sub(r'https?://[^\s]+', '', clean_search)
    clean_search = re.sub(r'doi:[^\s]+', '', clean_search, flags=re.IGNORECASE)
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(clean_search[:200])}&rows=3"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                t = item.get('title', [''])[0]
                d = item.get('DOI', '')
                if t and d:
                    sim = title_similarity(clean_search, t)
                    results.append({'title': t, 'doi': d, 'similarity': sim})
            return results
    except Exception as e:
        return []

# Load Chapter 9 references from ch09_refs_raw.json
ch9_json_path = os.path.join(workspace_dir, ".agents", "teamwork_preview_worker_m2_2", "ch09_refs_raw.json")
with open(ch9_json_path, "r", encoding="utf-8") as f:
    ch9_raw_data = json.load(f)

chapters_to_process = [f"chapter_{str(i).zfill(2)}.html" for i in range(8, 15)]
audit_summary = {}

for ch_file in chapters_to_process:
    file_path = os.path.join(chapters_dir, ch_file)
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    ref_items = []
    
    if ch_file == "chapter_09.html":
        # Using extracted 17 items
        for item in ch9_raw_data:
            item_soup = BeautifulSoup(item['raw_html'], "html.parser")
            ref_items.append({'raw_html': item['raw_html'], 'text': item['text'], 'elem': item_soup})
    elif ch_file == "chapter_11.html":
        # Extract <p> items under References
        ref_heading = soup.find(string=re.compile(r'References', re.I))
        parent = ref_heading.parent if ref_heading else None
        while parent and parent.name not in ['p', 'h1', 'h2', 'h3', 'h4', 'div']:
            parent = parent.parent
        curr = parent.find_next_sibling() if parent else None
        while curr:
            if curr.name == "p":
                txt = curr.get_text(strip=True)
                if re.match(r'^\d+\.\s', txt):
                    ref_items.append({'raw_html': str(curr), 'text': txt, 'elem': curr})
                elif not txt:
                    pass
                else:
                    break
            else:
                break
            curr = curr.find_next_sibling()
    else:
        # standard <ol> items
        next_ol = soup.find("ol")
        # Ensure it's the reference ol (if multiple ols exist, find the one after References)
        ref_heading = soup.find(string=re.compile(r'References', re.I))
        if ref_heading:
            parent = ref_heading.parent
            while parent and parent.name not in ['p', 'h1', 'h2', 'h3', 'h4', 'div']:
                parent = parent.parent
            if parent:
                next_ol = parent.find_next("ol")
        if next_ol:
            for li in next_ol.find_all("li", recursive=False):
                ref_items.append({'raw_html': str(li), 'text': li.get_text(strip=True), 'elem': li})
                
    print(f"\nProcessing {ch_file}: {len(ref_items)} items")
    ch_results = []
    
    for idx, r in enumerate(ref_items, 1):
        txt = r['text']
        raw = r['raw_html']
        elem = r['elem']
        
        # Check existing DOIs
        extracted_dois = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', raw)
        clean_dois = [d.rstrip('.,;)"\'<>') for d in extracted_dois]
        clean_dois = list(dict.fromkeys(clean_dois)) # deduplicate
        
        existing_doi = clean_dois[0] if clean_dois else None
        doi_status = "UNKNOWN"
        doi_info = None
        verified_doi = None
        
        if existing_doi:
            doi_info = check_doi_crossref(existing_doi)
            if doi_info['valid']:
                sim = title_similarity(txt, doi_info['title'])
                if sim >= 0.35:
                    doi_status = "OK"
                    verified_doi = doi_info['clean_doi']
                else:
                    doi_status = "HALLUCINATED"
            else:
                doi_status = "BROKEN"
        else:
            doi_status = "MISSING"
            
        # Search CrossRef if missing, broken, or hallucinated
        candidate = None
        if doi_status in ["MISSING", "BROKEN", "HALLUCINATED"]:
            cands = search_crossref(txt)
            if cands:
                top = cands[0]
                if top['similarity'] >= 0.45: # Strict title matching
                    candidate = top
                    verified_doi = top['doi']
                    
        item_res = {
            'index': idx,
            'text': txt[:120] + "...",
            'full_text': txt,
            'raw_html': raw,
            'existing_doi': existing_doi,
            'doi_status': doi_status,
            'doi_info': doi_info,
            'candidate': candidate,
            'final_doi': verified_doi
        }
        ch_results.append(item_res)
        print(f"  Ref {idx}: status={doi_status}, existing={existing_doi}, final_doi={verified_doi}")
        
    audit_summary[ch_file] = ch_results

with open(os.path.join(workspace_dir, ".agents", "teamwork_preview_worker_m2_2", "audit_report_detailed.json"), "w", encoding="utf-8") as f:
    json.dump(audit_summary, f, indent=2)

print("\nAudit completed and saved to audit_report_detailed.json")
