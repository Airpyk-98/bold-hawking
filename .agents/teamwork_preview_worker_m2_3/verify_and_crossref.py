import os
import json
import re
import urllib.request
import urllib.parse

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3"
json_path = os.path.join(base_dir, "refs_dump_15_20.json")

with open(json_path, "r", encoding="utf-8") as f:
    refs = json.load(f)

print(f"Total references loaded: {len(refs)}")

def normalize_title(t):
    t = re.sub(r'[^\w\s]', '', t.lower())
    return " ".join(t.split())

def title_similarity(t1, t2):
    n1, n2 = normalize_title(t1), normalize_title(t2)
    if not n1 or not n2:
        return 0.0
    words1 = set(n1.split())
    words2 = set(n2.split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0.0

verification_results = []

for r in refs:
    ch = r["chapter"]
    ref_num = r["ref_num"]
    text = r["text"]
    hrefs = r["hrefs"]
    nested = r["nested"]
    
    # Extract DOI from href or text
    doi_match = None
    for h in hrefs:
        m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', h)
        if m:
            doi_match = m.group(0).rstrip('.,;)')
            break
    if not doi_match:
        m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
        if m:
            doi_match = m.group(0).rstrip('.,;)')
            
    print(f"Checking Ch {ch} Ref {ref_num} | Existing DOI: {doi_match}")
    
    # Query CrossRef API with text snippet
    # Clean text to form a query title
    # Remove author year prefix if possible
    query_str = text
    # try to extract title from text (often between (year). and period)
    title_match = re.search(r'\(\d{4}\)\.\s*([^.]+)\.', text)
    extracted_title = title_match.group(1).strip() if title_match else text[:100]
    
    crossref_doi = None
    crossref_title = None
    sim_score = 0.0
    status_code = None
    
    if doi_match:
        # Check direct metadata of existing DOI via Crossref API
        try:
            url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_match)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.getcode()
                if status_code == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    item = data.get('message', {})
                    titles = item.get('title', [])
                    crossref_title = titles[0] if titles else ""
                    sim_score = title_similarity(extracted_title, crossref_title)
        except urllib.error.HTTPError as e:
            status_code = e.code
        except Exception as e:
            status_code = str(e)
            
    # Search Crossref by bibliographic text to verify or find true DOI
    search_doi = None
    search_title = None
    search_sim = 0.0
    try:
        url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(extracted_title)}&rows=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            if items:
                search_doi = items[0].get('DOI')
                titles = items[0].get('title', [])
                search_title = titles[0] if titles else ""
                search_sim = title_similarity(extracted_title, search_title)
    except Exception as e:
        print(f"  Search error: {e}")

    result_item = {
        "chapter": ch,
        "ref_num": ref_num,
        "text": text,
        "extracted_title": extracted_title,
        "nested": nested,
        "hrefs": hrefs,
        "existing_doi": doi_match,
        "existing_doi_status": status_code,
        "existing_doi_title": crossref_title,
        "existing_doi_title_sim": sim_score,
        "search_doi": search_doi,
        "search_title": search_title,
        "search_sim": search_sim
    }
    verification_results.append(result_item)

out_res = os.path.join(base_dir, "verification_audit_results.json")
with open(out_res, "w", encoding="utf-8") as f:
    json.dump(verification_results, f, indent=2, ensure_ascii=False)

print(f"Saved audit results to {out_res}")
