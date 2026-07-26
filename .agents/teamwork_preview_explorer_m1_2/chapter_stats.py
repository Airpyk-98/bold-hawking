import json

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\verification_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"{'Chapter':<15} | {'Total Refs':<10} | {'Valid DOI':<10} | {'Hallucinated':<12} | {'Broken HTTP':<12} | {'Missing DOI':<12} | {'Malformed HTML':<14}")
print("-" * 95)

total_refs_all = 0
total_ok = 0
total_hallucinated = 0
total_broken = 0
total_missing = 0
total_malformed_html = 0

for ch_file, ch_data in data.items():
    items = ch_data.get("items", [])
    tot = len(items)
    ok_cnt = sum(1 for i in items if i["doi_status"] == "OK")
    hal_cnt = sum(1 for i in items if i["doi_status"] == "HALLUCINATED")
    brk_cnt = sum(1 for i in items if i["doi_status"] == "BROKEN_HTTP")
    mis_cnt = sum(1 for i in items if i["doi_status"] == "MISSING")
    
    mal_html_cnt = sum(1 for i in items if len(i.get("formatting_issues", [])) > 0)
    
    total_refs_all += tot
    total_ok += ok_cnt
    total_hallucinated += hal_cnt
    total_broken += brk_cnt
    total_missing += mis_cnt
    total_malformed_html += mal_html_cnt
    
    print(f"{ch_file:<15} | {tot:<10} | {ok_cnt:<10} | {hal_cnt:<12} | {brk_cnt:<12} | {mis_cnt:<12} | {mal_html_cnt:<14}")

print("-" * 95)
print(f"{'TOTAL':<15} | {total_refs_all:<10} | {total_ok:<10} | {total_hallucinated:<12} | {total_broken:<12} | {total_missing:<12} | {total_malformed_html:<14}")
