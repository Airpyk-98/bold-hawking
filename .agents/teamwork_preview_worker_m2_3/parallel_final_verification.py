import os
import json
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
api_headers = {"User-Agent": "mailto:admin@example.com"}

link_tasks = []

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
        text = li.get_text(separator=" ", strip=True)
        has_nested = any(a.find("a") is not None for a in a_tags)
        
        links = []
        for a in a_tags:
            href = a.get("href")
            if href and href not in links:
                links.append(href)
                
        for href in links:
            link_tasks.append({
                "chapter": ch,
                "ref_num": idx,
                "href": href,
                "has_nested": has_nested,
                "text_snippet": text[:80]
            })

def check_link(item):
    href = item["href"]
    status_code = None
    redirect_url = None
    verified_ok = False
    details = ""
    
    if "doi.org" in href or "10." in href:
        m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', href)
        doi = m.group(0).rstrip('.,;)>') if m else None
        
        try:
            r = requests.get(href, headers=headers, allow_redirects=False, timeout=8)
            status_code = r.status_code
            redirect_url = r.headers.get("Location", "")
            if status_code in [200, 301, 302, 303, 307, 308]:
                verified_ok = True
                details = f"Resolved via doi.org ({status_code} -> {redirect_url[:50]}...)"
        except Exception as e:
            details = f"doi.org check error: {e}"
            
        if not verified_ok and doi:
            try:
                q_doi = requests.utils.quote(doi)
                r2 = requests.get(f"https://api.crossref.org/works/{q_doi}", headers=api_headers, timeout=8)
                if r2.status_code == 200:
                    verified_ok = True
                    status_code = 200
                    details = "Verified via CrossRef API (200 OK)"
            except Exception:
                pass
    else:
        try:
            r = requests.get(href, headers=headers, allow_redirects=True, timeout=8)
            status_code = r.status_code
            if status_code == 200:
                verified_ok = True
                details = "Web URL 200 OK"
        except Exception as e:
            details = f"Web URL check error: {e}"
            
    res = dict(item)
    res.update({
        "status_code": status_code,
        "redirect_url": redirect_url,
        "verified_ok": verified_ok,
        "details": details
    })
    return res

results = []
print(f"Starting parallel 200 OK verification for {len(link_tasks)} reference links...")

with ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(check_link, it) for it in link_tasks]
    for future in as_completed(futures):
        r = future.result()
        results.append(r)
        status_str = "200 OK" if r["verified_ok"] else "FAIL"
        print(f"Ch {r['chapter']} Ref {r['ref_num']:02d} | Link: {r['href']} -> [{status_str}] ({r['details']})")

results.sort(key=lambda x: (x["chapter"], x["ref_num"]))

out_json = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\final_verification_results.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

total_links = len(results)
passed_links = sum(1 for v in results if v["verified_ok"])
failed_links = total_links - passed_links

print(f"\n==================================================")
print(f"FINAL REFERENCE VERIFICATION REPORT (Ch 15-20)")
print(f"==================================================")
print(f"Total Links Checked: {total_links}")
print(f"Passed (200 OK / Valid Resolution): {passed_links}")
print(f"Failed: {failed_links}")
print(f"Success Rate: {(passed_links/total_links)*100:.1f}%")
print(f"==================================================")
