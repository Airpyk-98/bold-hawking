import json
import os

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\verification_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

out_file = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\summary_report.txt"

with open(out_file, "w", encoding="utf-8") as out:
    out.write("=== SUMMARY OF CHAPTERS 8 - 14 ===\n\n")

    for ch_file, ch_data in data.items():
        out.write(f"==================================================\n")
        out.write(f"File: {ch_file}\n")
        out.write(f"Header: {ch_data.get('refs_header_text')}\n")
        out.write(f"Total References Found in HTML: {ch_data.get('total_references')}\n")
        out.write(f"==================================================\n\n")
        
        items = ch_data.get("items", [])
        if not items:
            out.write("  NO REFERENCE ITEMS FOUND IN THIS CHAPTER!\n\n")
            continue
            
        for item in items:
            out.write(f"--- Ref #{item['index']} ---\n")
            out.write(f"Text: {item['text']}\n")
            out.write(f"Raw HTML: {item['raw_html']}\n")
            out.write(f"DOI Status: {item['doi_status']}\n")
            if item.get("existing_doi"):
                out.write(f"Existing DOI: {item['existing_doi']}\n")
                cr = item.get("crossref_match_for_existing_doi")
                if cr and cr.get("valid"):
                    out.write(f"  CrossRef Title for Existing DOI: {cr.get('title')}\n")
                    out.write(f"  CrossRef Authors: {', '.join(cr.get('authors', []))}\n")
                    out.write(f"  CrossRef Year: {cr.get('year')}\n")
                elif cr:
                    out.write(f"  CrossRef Validation Failed: {cr.get('status', cr.get('error'))}\n")
            
            if item.get("formatting_issues"):
                out.write("Formatting Issues:\n")
                for fi in item["formatting_issues"]:
                    out.write(f"  - {fi}\n")
                    
            if item.get("doi_issues"):
                out.write("DOI Issues:\n")
                for di in item["doi_issues"]:
                    out.write(f"  - {di}\n")
                    
            if item.get("suggested_doi"):
                out.write(f"Suggested Correct DOI (from CrossRef Search): {item['suggested_doi']}\n")
                cand = item.get("crossref_search_candidates", [])
                if cand:
                    out.write(f"  Suggested Paper Title: {cand[0].get('title')}\n")
                    out.write(f"  Suggested Paper Year: {cand[0].get('year')}\n")
            out.write("\n")

print("Wrote summary_report.txt successfully!")
