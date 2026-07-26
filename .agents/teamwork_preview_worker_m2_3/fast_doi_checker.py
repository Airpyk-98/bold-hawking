import json
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\doi_summary.json", "r", encoding="utf-8") as f:
    items = json.load(f)

def normalize_text(s):
    if not s: return ""
    s = re.sub(r'[^\w\s]', '', s.lower())
    return " ".join(s.split())

def title_sim(t1, t2):
    n1, n2 = normalize_text(t1), normalize_text(t2)
    if not n1 or not n2: return 0.0
    w1, w2 = set(n1.split()), set(n2.split())
    u = w1.union(w2)
    return len(w1.intersection(w2)) / len(u) if u else 0.0

def check_item(item):
    ch = item["chapter"]
    num = item["ref_num"]
    doi = item["doi"]
    title = item["title"]
    hrefs = item["hrefs"]
    text = item["text"]
    
    result = {
        "chapter": ch,
        "ref_num": num,
        "cited_title": title,
        "existing_doi": doi,
        "hrefs": hrefs,
        "crossref_status": None,
        "doi_org_status": None,
        "crossref_title": None,
        "sim_score": 0.0,
        "search_doi": None,
        "search_title": None,
        "search_sim": 0.0,
        "notes": []
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    if doi:
        # Check Crossref API
        try:
            r = requests.get(f"https://api.crossref.org/works/{doi}", headers={"User-Agent": "mailto:admin@example.com"}, timeout=8)
            result["crossref_status"] = r.status_code
            if r.status_code == 200:
                msg = r.json().get("message", {})
                titles = msg.get("title", [])
                result["crossref_title"] = titles[0] if titles else ""
                result["sim_score"] = title_sim(title, result["crossref_title"])
        except Exception as e:
            result["crossref_status"] = str(e)
            
        # Check doi.org resolution
        try:
            r2 = requests.get(f"https://doi.org/{doi}", headers=headers, allow_redirects=False, timeout=8)
            result["doi_org_status"] = r2.status_code
        except Exception as e:
            result["doi_org_status"] = str(e)
    
    # Also do bibliographic search on Crossref if no doi or if sim score < 0.5
    if not doi or result["sim_score"] < 0.5:
        try:
            r3 = requests.get(f"https://api.crossref.org/works?query.bibliographic={requests.utils.quote(title)}&rows=1", headers={"User-Agent": "mailto:admin@example.com"}, timeout=8)
            if r3.status_code == 200:
                items_res = r3.json().get("message", {}).get("items", [])
                if items_res:
                    result["search_doi"] = items_res[0].get("DOI")
                    st = items_res[0].get("title", [])
                    result["search_title"] = st[0] if st else ""
                    result["search_sim"] = title_sim(title, result["search_title"])
        except Exception as e:
            pass
            
    return result

results = []
print(f"Starting parallel check of {len(items)} references...")
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_item, it) for it in items]
    for future in as_completed(futures):
        res = future.result()
        results.append(res)
        ch, num = res["chapter"], res["ref_num"]
        doi = res["existing_doi"]
        cr_st = res["crossref_status"]
        doi_st = res["doi_org_status"]
        sim = res["sim_score"]
        search_sim = res["search_sim"]
        search_doi = res["search_doi"]
        
        flag = "OK"
        if doi and (cr_st != 200 or doi_st not in [200, 301, 302, 303, 307, 308] or sim < 0.5):
            flag = "WARNING / MISMATCH"
        print(f"Ch {ch} Ref {num:02d} | DOI: {doi} | CR: {cr_st} | DOI.org: {doi_st} | Sim: {sim:.2f} | SearchSim: {search_sim:.2f} -> [{flag}]")

results.sort(key=lambda x: (x["chapter"], x["ref_num"]))
with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\fast_check_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Fast check complete. Results saved.")
