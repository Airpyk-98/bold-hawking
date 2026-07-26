import json
import os

with open(r'C:\Users\DELL\Documents\antigravity\bold-hawking\full_doi_audit.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

print(f"Total audit items: {len(audit_data)}")

for item in audit_data:
    ch = item['chapter']
    rnum = item['ref_num']
    doi = item['existing_doi']
    status = item['status']
    title = item['verified_title']
    cand = item['candidate']
    nested = item['has_nested_a']
    
    print(f"Ch{ch} Ref{rnum:02d} | Nested={nested} | DOI={doi} | Status={status}")
    if status == 200:
        print(f"   CrossRef Title: {title}")
    elif cand:
        print(f"   Candidate DOI: {cand['doi']} (score={cand['score']:.2f}) Title: {cand['title']}")
    else:
        print(f"   Text: {item['text'][:80]}...")
