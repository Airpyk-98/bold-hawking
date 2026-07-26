import json
import re

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\refs_dump_15_20.json", "r", encoding="utf-8") as f:
    refs = json.load(f)

print(f"Loaded {len(refs)} references.")

nested_count = 0
ch20_numbered_count = 0

for r in refs:
    ch = r["chapter"]
    ref_num = r["ref_num"]
    nested = r["nested"]
    hrefs = r["hrefs"]
    text = r["text"]
    raw = r["raw_html"]
    
    if nested:
        nested_count += 1
    if ch == 20 and re.match(r'^\s*\d+\.\s*', text):
        ch20_numbered_count += 1
        
    # Check chapter 15 ref 10
    if ch == 15 and ref_num == 10:
        print("=== Ch 15 Ref 10 RAW HTML ===")
        print(raw)
        print("HREFS:", hrefs)

    # Check chapter 20 ref 4
    if ch == 20 and ref_num == 4:
        print("=== Ch 20 Ref 4 RAW HTML ===")
        print(raw)

    # Check chapter 20 ref 2
    if ch == 20 and ref_num == 2:
        print("=== Ch 20 Ref 2 RAW HTML ===")
        print(raw)

print(f"Total nested anchor tags: {nested_count}")
print(f"Chapter 20 hardcoded leading numbers: {ch20_numbered_count}")
