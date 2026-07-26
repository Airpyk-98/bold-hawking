import json

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\investigation_report.json", "r", encoding="utf-8") as f:
    report = json.load(f)

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\investigation_summary.txt", "w", encoding="utf-8") as out:
    out.write(f"Loaded {len(report)} items from investigation report:\n\n")
    for item in report:
        ch = item["chapter"]
        num = item["ref_num"]
        doi = item["existing_doi"]
        hrefs = item["existing_hrefs"]
        text = item["full_text"]
        cands = item["candidates"]
        
        out.write(f"=== Ch {ch} Ref {num:02d} ===\n")
        out.write(f"Full text: {text}\n")
        out.write(f"Existing DOI: {doi}\n")
        out.write(f"Existing HREFs: {hrefs}\n")
        out.write("Candidates:\n")
        for idx, c in enumerate(cands, 1):
            out.write(f"  [{idx}] DOI: {c['doi']} | Author: {c['author']} | Journal: {c['container']}\n")
            out.write(f"      Title: {c['title']}\n")
        out.write("-" * 70 + "\n")

print("Wrote investigation_summary.txt successfully.")
