import json
import re
import requests

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\discrepancies.json", "r", encoding="utf-8") as f:
    discrepancies = json.load(f)

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\refs_dump_15_20.json", "r", encoding="utf-8") as rf:
    all_refs = json.load(rf)

headers = {"User-Agent": "mailto:admin@example.com"}
report = []

for item in discrepancies:
    ch = item["chapter"]
    num = item["ref_num"]
    cited_title = item["cited_title"]
    doi = item["existing_doi"]
    
    ref_obj = next(r for r in all_refs if r["chapter"] == ch and r["ref_num"] == num)
    ref_text = ref_obj["text"]
    
    # Query CrossRef for full bibliographic search using text snippet
    q = requests.utils.quote(ref_text[:200])
    candidates = []
    try:
        res = requests.get(f"https://api.crossref.org/works?query.bibliographic={q}&rows=3", headers=headers, timeout=10)
        if res.status_code == 200:
            items = res.json().get("message", {}).get("items", [])
            for it in items:
                c_doi = it.get("DOI")
                c_title = it.get("title", [""])[0]
                c_author = it.get("author", [{}])[0].get("family", "") if it.get("author") else ""
                c_container = it.get("container-title", [""])[0] if it.get("container-title") else ""
                candidates.append({
                    "doi": c_doi,
                    "title": c_title,
                    "author": c_author,
                    "container": c_container
                })
    except Exception as e:
        print(f"Error on Ch {ch} Ref {num}: {e}")

    report.append({
        "chapter": ch,
        "ref_num": num,
        "cited_title": cited_title,
        "existing_doi": doi,
        "existing_hrefs": item["hrefs"],
        "full_text": ref_text,
        "candidates": candidates
    })

out_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\investigation_report.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"Investigation complete. Report saved to {out_path}")
