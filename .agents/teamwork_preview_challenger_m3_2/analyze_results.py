import json
import os

res_file = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_challenger_m3_2\verification_results.json"
with open(res_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

total_chaps = len(data)
total_refs = 0
total_dois = 0
valid_dois = 0
dead_dois = 0
mismatches = []
matches = []

for chap in data:
    chap_name = chap['chapter']
    refs = chap['references']
    total_refs += chap['ref_count']
    
    for ref in refs:
        ref_num = ref['ref_num']
        text = ref['text']
        checks = ref.get('crossref_checks', [])
        
        for c in checks:
            total_dois += 1
            doi = c['doi']
            cr = c['crossref_data']
            sim = c['similarity']
            status = cr.get('status', 'UNKNOWN')
            
            if status == 'OK':
                valid_dois += 1
                cr_title = cr.get('title', '')
                if sim >= 0.50:
                    matches.append({
                        'chap': chap_name,
                        'ref_num': ref_num,
                        'doi': doi,
                        'cited': text,
                        'cr_title': cr_title,
                        'sim': sim
                    })
                else:
                    mismatches.append({
                        'chap': chap_name,
                        'ref_num': ref_num,
                        'doi': doi,
                        'cited': text,
                        'cr_title': cr_title,
                        'sim': sim,
                        'reason': 'MISMATCHED_TITLE'
                    })
            else:
                dead_dois += 1
                mismatches.append({
                    'chap': chap_name,
                    'ref_num': ref_num,
                    'doi': doi,
                    'cited': text,
                    'cr_title': '',
                    'sim': 0.0,
                    'reason': f"DEAD_DOI_{status}"
                })

print("================ EMPIRICAL AUDIT RESULTS ================")
print(f"Chapters Processed: {total_chaps} (chapter_01.html to chapter_20.html)")
print(f"Total References Found: {total_refs}")
print(f"Total DOIs Extracted & Checked: {total_dois}")
print(f"Valid DOIs (CrossRef 200 OK): {valid_dois}")
print(f"Dead / Broken DOIs (404/Error): {dead_dois}")
print(f"Verified Title Matches (Similarity >= 0.50): {len(matches)}")
print(f"Mismatched / Hallucinated DOIs: {len(mismatches)}")

if mismatches:
    print("\n--- DETAILED MISMATCH / DEAD DOI LIST ---")
    for m in mismatches:
        print(f"Chapter: {m['chap']} | Ref: #{m['ref_num']} | DOI: {m['doi']}")
        print(f"  Reason: {m['reason']}")
        print(f"  Cited Text: {m['cited'][:120]}...")
        if m['cr_title']:
            print(f"  CrossRef Title: {m['cr_title']}")
        print(f"  Similarity Score: {m['sim']:.2f}")
        print("-" * 60)
