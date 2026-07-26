import json
import os

audit_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\full_audit_results.json"
out_summary = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\full_audit_summary.md"

if not os.path.exists(audit_path):
    print("Audit path does not exist yet.")
    exit(0)

with open(audit_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(out_summary, "w", encoding="utf-8") as out:
    out.write("# Detailed Reference Audit Summary (Chapters 8-14)\n\n")
    
    total_chapters = len(data)
    total_refs = sum(ch["total_references"] for ch in data.values())
    total_ok = sum(sum(1 for r in ch["references"] if r["doi_status"] == "OK") for ch in data.values())
    total_hallucinated = sum(sum(1 for r in ch["references"] if r["doi_status"] == "HALLUCINATED") for ch in data.values())
    total_broken = sum(sum(1 for r in ch["references"] if r["doi_status"] == "BROKEN_HTTP") for ch in data.values())
    total_missing = sum(sum(1 for r in ch["references"] if r["doi_status"] == "MISSING") for ch in data.values())
    total_malformed = sum(sum(1 for r in ch["references"] if len(r.get("formatting_issues", [])) > 0) for ch in data.values())
    
    out.write("## Overview Metrics\n\n")
    out.write(f"- **Total Chapters Audited**: {total_chapters} (Chapters 8 through 14)\n")
    out.write(f"- **Total Reference Items Found**: {total_refs}\n")
    out.write(f"- **Valid & Verified DOIs**: {total_ok}\n")
    out.write(f"- **Hallucinated DOIs**: {total_hallucinated}\n")
    out.write(f"- **Broken/Non-functional DOIs**: {total_broken}\n")
    out.write(f"- **Missing DOIs/URLs**: {total_missing}\n")
    out.write(f"- **Malformed HTML Anchor Tags**: {total_malformed}\n\n")
    
    out.write("## Chapter Breakdown Table\n\n")
    out.write("| Chapter | Container Type | Total Refs | Valid DOI | Hallucinated | Broken HTTP | Missing DOI | Malformed HTML |\n")
    out.write("|---|---|---|---|---|---|---|---|\n")
    
    for ch_file, ch_data in data.items():
        refs = ch_data.get("references", [])
        tot = len(refs)
        c_type = ch_data.get("container_type", "UNKNOWN")
        ok_c = sum(1 for r in refs if r["doi_status"] == "OK")
        hal_c = sum(1 for r in refs if r["doi_status"] == "HALLUCINATED")
        brk_c = sum(1 for r in refs if r["doi_status"] == "BROKEN_HTTP")
        mis_c = sum(1 for r in refs if r["doi_status"] == "MISSING")
        mal_c = sum(1 for r in refs if len(r.get("formatting_issues", [])) > 0)
        out.write(f"| {ch_file} | `{c_type}` | {tot} | {ok_c} | {hal_c} | {brk_c} | {mis_c} | {mal_c} |\n")
        
    out.write("\n\n## Per-Chapter Detailed Findings\n\n")
    
    for ch_file, ch_data in data.items():
        out.write(f"### {ch_file}\n")
        out.write(f"- **Reference Heading Found**: {ch_data.get('heading_found')} (`<{ch_data.get('heading_tag')}>`)\n")
        out.write(f"- **HTML Structure Type**: `{ch_data.get('container_type')}`\n")
        out.write(f"- **Total References**: {ch_data.get('total_references')}\n\n")
        
        refs = ch_data.get("references", [])
        if not refs:
            out.write("  *No reference items found in this chapter file!*\n\n")
            continue
            
        for r in refs:
            out.write(f"#### Reference #{r['index']}\n")
            out.write(f"- **Text**: {r['text']}\n")
            out.write(f"- **DOI Status**: `{r['doi_status']}`\n")
            if r.get("existing_doi"):
                out.write(f"- **Existing DOI**: `{r['existing_doi']}`\n")
                cr = r.get("crossref_doi_info")
                if cr and cr.get("valid"):
                    out.write(f"  - **CrossRef Title**: {cr.get('title')}\n")
                    out.write(f"  - **CrossRef Authors**: {', '.join(cr.get('authors', []))}\n")
                    out.write(f"  - **CrossRef Year**: {cr.get('year')}\n")
                elif cr:
                    out.write(f"  - **CrossRef Error**: {cr.get('status', cr.get('error'))}\n")
            
            if r.get("formatting_issues"):
                out.write("- **Formatting Issues**:\n")
                for fi in r["formatting_issues"]:
                    out.write(f"  - ⚠️ {fi}\n")
                    
            if r.get("doi_issues"):
                out.write("- **DOI Issues**:\n")
                for di in r["doi_issues"]:
                    out.write(f"  - ❌ {di}\n")
                    
            if r.get("suggested_doi"):
                out.write(f"- **Suggested DOI**: [{r['suggested_doi']}]({r['suggested_doi']})\n")
                if r.get("search_candidates"):
                    cand = r["search_candidates"][0]
                    out.write(f"  - **Matched Title**: {cand.get('title')}\n")
                    out.write(f"  - **Matched Year**: {cand.get('year')}\n")
            out.write("\n")

print("Generated full_audit_summary.md")
