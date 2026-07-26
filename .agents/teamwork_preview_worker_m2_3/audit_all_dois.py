import json
import re
import requests

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\refs_dump_15_20.json", "r", encoding="utf-8") as f:
    refs = json.load(f)

print(f"Total references: {len(refs)}")

doi_summary = []

for r in refs:
    ch = r["chapter"]
    num = r["ref_num"]
    text = r["text"]
    hrefs = r["hrefs"]
    
    # Extract DOI from hrefs or text
    doi = None
    for h in hrefs:
        m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', h)
        if m:
            doi = m.group(0).rstrip('.,;)>')
            break
    if not doi:
        m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
        if m:
            doi = m.group(0).rstrip('.,;)>')
            
    # Extract title snippet
    tm = re.search(r'\(\d{4}[a-z]?\)\.\s*([^.]+)\.', text)
    title = tm.group(1).strip() if tm else text[:60]
    
    doi_summary.append({
        "chapter": ch,
        "ref_num": num,
        "title": title,
        "doi": doi,
        "hrefs": hrefs,
        "text": text
    })

print(f"Total entries with DOIs: {sum(1 for d in doi_summary if d['doi'])}")
print(f"Total entries without DOIs: {sum(1 for d in doi_summary if not d['doi'])}")

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\doi_summary.json", "w", encoding="utf-8") as f:
    json.dump(doi_summary, f, indent=2, ensure_ascii=False)
