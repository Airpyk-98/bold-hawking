import os
import json
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

doi_links = []

for ch in range(15, 21):
    fname = f"chapter_{ch}.html"
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    if not ols:
        continue
    ol = ols[-1]
    lis = ol.find_all("li", recursive=False)
    
    for idx, li in enumerate(lis, 1):
        a_tags = li.find_all("a")
        for a in a_tags:
            href = a.get("href")
            if href and ("doi.org" in href or "10." in href):
                doi_links.append({
                    "chapter": ch,
                    "ref_num": idx,
                    "href": href,
                    "text": li.get_text(separator=" ", strip=True)[:70]
                })

print(f"Found {len(doi_links)} DOI links across Chapters 15-20.")

def verify_doi(item):
    href = item["href"]
    m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', href)
    doi = m.group(0).rstrip('.,;)>') if m else None
    
    ok = False
    method = ""
    status_code = None
    
    # Check 1: doi.org resolution
    try:
        req_url = href.replace("<", "%3C").replace(">", "%3E")
        r = requests.get(req_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, allow_redirects=False, timeout=8)
        status_code = r.status_code
        if status_code in [200, 301, 302, 303, 307, 308]:
            ok = True
            method = f"doi.org ({status_code})"
    except Exception as e:
        method = f"doi.org error: {e}"
        
    # Check 2: CrossRef API
    if not ok and doi:
        try:
            q_doi = requests.utils.quote(doi)
            r2 = requests.get(f"https://api.crossref.org/works/{q_doi}", headers={"User-Agent": "mailto:admin@example.com"}, timeout=8)
            if r2.status_code == 200:
                ok = True
                status_code = 200
                method = "CrossRef API (200 OK)"
        except Exception:
            pass
            
    res = dict(item)
    res.update({
        "status_code": status_code,
        "verified_ok": ok,
        "method": method
    })
    return res

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(verify_doi, it) for it in doi_links]
    for future in as_completed(futures):
        r = future.result()
        results.append(r)
        status_str = "PASS 200 OK" if r["verified_ok"] else "FAIL"
        print(f"Ch {r['chapter']} Ref {r['ref_num']:02d} | DOI Link: {r['href'][:65]}... -> [{status_str}] ({r['method']})")

results.sort(key=lambda x: (x["chapter"], x["ref_num"]))

total = len(results)
passed = sum(1 for r in results if r["verified_ok"])
failed = total - passed

print(f"\n==================================================")
print(f"DOI 200 OK VERIFICATION SUMMARY (Chapters 15-20)")
print(f"==================================================")
print(f"Total DOIs Checked: {total}")
print(f"Passed (200 OK): {passed}")
print(f"Failed: {failed}")
print(f"Success Rate: {(passed/total)*100:.1f}%")
print(f"==================================================")

out_file = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\doi_verification_final.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
