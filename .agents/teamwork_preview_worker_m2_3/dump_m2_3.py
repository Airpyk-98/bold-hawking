import os
import json
from bs4 import BeautifulSoup

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

results = []

for ch in range(15, 21):
    fname = f"chapter_{ch}.html"
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    ols = soup.find_all("ol")
    if not ols:
        print(f"ERROR: No <ol> in {fname}")
        continue
    ol = ols[-1]
    lis = ol.find_all("li", recursive=False)
    for i, li in enumerate(lis, 1):
        a_tags = li.find_all("a")
        nested = any(a.find("a") is not None for a in a_tags)
        text = li.get_text(separator=" ", strip=True)
        raw_html = str(li)
        
        hrefs = []
        for a in a_tags:
            h = a.get("href")
            if h and h not in hrefs:
                hrefs.append(h)
                
        ref_info = {
            "chapter": ch,
            "ref_num": i,
            "nested": nested,
            "a_count": len(a_tags),
            "hrefs": hrefs,
            "text": text,
            "raw_html": raw_html
        }
        results.append(ref_info)

out_file = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\refs_dump_15_20.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Successfully dumped {len(results)} references across Ch 15-20 to {out_file}")
