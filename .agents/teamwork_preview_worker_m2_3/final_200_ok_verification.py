import os
import json
import re
import requests
from bs4 import BeautifulSoup

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

verification_list = []

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
api_headers = {"User-Agent": "mailto:admin@example.com"}

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
        
        # Check nested tags count
        has_nested = any(a.find("a") is not None for a in a_tags)
        
        links = []
        for a in a_tags:
            href = a.get("href")
            if href and href not in links:
                links.append(href)
                
        for href in links:
            status_code = None
            redirect_url = None
            verified_ok = False
            details = ""
            
            if "doi.org" in href or "10." in href:
                # Extract DOI
                m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', href)
                doi = m.group(0).rstrip('.,;)>') if m else None
                
                # Method 1: Check doi.org redirect resolution
                try:
                    r = requests.get(href, headers=headers, allow_redirects=False, timeout=10)
                    status_code = r.status_code
                    redirect_url = r.headers.get("Location", "")
                    if status_code in [200, 301, 302, 303, 307, 308]:
                        verified_ok = True
                        details = f"Resolved via doi.org ({status_code} -> {redirect_url[:50]}...)"
                except Exception as e:
                    details = f"doi.org check error: {e}"
                    
                # Method 2: If doi.org returned 404 or error, verify via CrossRef API
                if not verified_ok and doi:
                    try:
                        q_doi = requests.utils.quote(doi)
                        r2 = requests.get(f"https://api.crossref.org/works/{q_doi}", headers=api_headers, timeout=10)
                        if r2.status_code == 200:
                            verified_ok = True
                            status_code = 200
                            details = "Verified via CrossRef API (200 OK)"
                    except Exception as e:
                        pass
            else:
                # Standard web URL check
                try:
                    r = requests.get(href, headers=headers, allow_redirects=True, timeout=10)
                    status_code = r.status_code
                    if status_code == 200:
                        verified_ok = True
                        details = "Web URL 200 OK"
                except Exception as e:
                    details = f"Web URL check error: {e}"
                    
            verification_list.append({
                "chapter": ch,
                "ref_num": idx,
                "href": href,
                "has_nested": has_nested,
                "status_code": status_code,
                "redirect_url": redirect_url,
                "verified_ok": verified_ok,
                "details": details,
                "text_snippet": text[:80]
            })

out_json = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\final_verification_results.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(verification_list, f, indent=2, ensure_ascii=False)

total_links = len(verification_list)
passed_links = sum(1 for v in verification_list if v["verified_ok"])
failed_links = total_links - passed_links

print(f"==================================================")
print(f"FINAL REFERENCE VERIFICATION REPORT (Ch 15-20)")
print(f"==================================================")
print(f"Total Links Checked: {total_links}")
print(f"Passed (200 OK / Valid Resolution): {passed_links}")
print(f"Failed: {failed_links}")
print(f"Success Rate: {(passed_links/total_links)*100:.1f}%")
print(f"==================================================")
