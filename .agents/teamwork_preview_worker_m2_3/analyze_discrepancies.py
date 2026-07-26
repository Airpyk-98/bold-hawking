import json

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\fast_check_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

mismatches = []
for r in results:
    doi = r["existing_doi"]
    cr = r["crossref_status"]
    doi_org = r["doi_org_status"]
    sim = r["sim_score"]
    
    if doi:
        if cr != 200 or doi_org not in [200, 301, 302, 303, 307, 308] or sim < 0.5:
            mismatches.append(r)

out_file = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\discrepancies.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(mismatches, f, indent=2, ensure_ascii=False)

print(f"Dumped {len(mismatches)} mismatches/warnings to {out_file}")
