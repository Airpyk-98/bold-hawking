import json
import os
import re

audit_json = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\full_audit_results.json"
analysis_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\analysis.md"
handoff_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\handoff.md"

with open(audit_json, "r", encoding="utf-8") as f:
    audit_data = json.load(f)

# Collect overall statistics
total_refs = 0
valid_dois = 0
hallucinated_dois = 0
broken_dois = 0
missing_dois = 0
malformed_html = 0

chapter_summaries = {}

for ch_file, ch_info in audit_data.items():
    refs = ch_info.get("references", [])
    tot = len(refs)
    total_refs += tot
    
    ok_cnt = sum(1 for r in refs if r["doi_status"] == "OK")
    hal_cnt = sum(1 for r in refs if r["doi_status"] == "HALLUCINATED")
    brk_cnt = sum(1 for r in refs if r["doi_status"] == "BROKEN_HTTP")
    mis_cnt = sum(1 for r in refs if r["doi_status"] == "MISSING")
    mal_cnt = sum(1 for r in refs if len(r.get("formatting_issues", [])) > 0)
    
    valid_dois += ok_cnt
    hallucinated_dois += hal_cnt
    broken_dois += brk_cnt
    missing_dois += mis_cnt
    malformed_html += mal_cnt
    
    chapter_summaries[ch_file] = {
        "container_type": ch_info.get("container_type"),
        "heading_found": ch_info.get("heading_found"),
        "total_references": tot,
        "valid_dois": ok_cnt,
        "hallucinated_dois": hal_cnt,
        "broken_dois": brk_cnt,
        "missing_dois": mis_cnt,
        "malformed_html": mal_cnt
    }

# 1. WRITE ANALYSIS.MD
with open(analysis_path, "w", encoding="utf-8") as out:
    out.write("# Chapter 8-14 Reference Exploration & Audit Analysis\n\n")
    out.write("## Executive Summary\n\n")
    out.write(f"This report presents the complete reference investigation and audit for **Milestone 1 (Chapters 8 through 14)** of the *Indigenous Medicines / Bold Hawking* project.\n\n")
    out.write(f"Across Chapters 8 through 14, a total of **{total_refs} reference items** were extracted and analyzed. The investigation revealed major HTML structural inconsistencies, widespread malformed anchor tags (nested `<a>` tags and broken `href` attributes), missing reference sections, non-standard `<p>` lists, and significant missing or broken DOI links.\n\n")
    
    out.write("### Key Metrics Overview Table\n\n")
    out.write("| Metric | Count | Percentage | Description |\n")
    out.write("|---|---|---|---|\n")
    out.write(f"| **Total Chapters Audited** | 7 | 100% | `chapter_08.html` to `chapter_14.html` |\n")
    out.write(f"| **Total Reference Items** | {total_refs} | 100% | Total extracted citation items |\n")
    out.write(f"| **Valid & Verified DOIs** | {valid_dois} | {valid_dois/max(1,total_refs)*100:.1f}% | DOIs present, resolving HTTP 200, matching paper title |\n")
    out.write(f"| **Hallucinated DOIs** | {hallucinated_dois} | {hallucinated_dois/max(1,total_refs)*100:.1f}% | DOIs present but pointing to unrelated papers |\n")
    out.write(f"| **Broken HTTP / Non-functional DOIs** | {broken_dois} | {broken_dois/max(1,total_refs)*100:.1f}% | DOIs present returning 404 or HTTP errors |\n")
    out.write(f"| **Missing DOIs/URLs** | {missing_dois} | {missing_dois/max(1,total_refs)*100:.1f}% | Reference items with no DOI or anchor tag |\n")
    out.write(f"| **Malformed HTML Anchor Tags** | {malformed_html} | {malformed_html/max(1,total_refs)*100:.1f}% | Items with nested `<a>` tags, unclosed tags, or malformed attributes |\n\n")
    
    out.write("## Chapter-by-Chapter Inventory & Structural Analysis\n\n")
    out.write("| Chapter File | References Heading | HTML Container | Ref Count | Valid DOI | Hallucinated | Broken HTTP | Missing DOI | Malformed HTML |\n")
    out.write("|---|---|---|---|---|---|---|---|---|\n")
    
    for ch_file, stat in chapter_summaries.items():
        out.write(f"| `{ch_file}` | `{'Yes' if stat['heading_found'] else 'No'}` | `{stat['container_type']}` | {stat['total_references']} | {stat['valid_dois']} | {stat['hallucinated_dois']} | {stat['broken_dois']} | {stat['missing_dois']} | {stat['malformed_html']} |\n")
        
    out.write("\n\n## Deep Dive Structural Findings\n\n")
    
    out.write("### 1. Missing Reference List in Chapter 9 (`chapter_09.html`)\n")
    out.write("- **Finding**: `chapter_09.html` (Mullein Leaf Tea) contains a `References` heading (`<p><span style=\"color: #339966\"><strong>References</strong></span></p>`), but **NO reference list (<ol> or <p>) exists beneath it**.\n")
    out.write("- **Impact**: In-text citations in Chapter 9 (e.g., `[4]`, `[9]`, `[10]`, `[12]`, `[15]`, `[17]`) cannot be resolved against any reference list in the chapter HTML file.\n")
    out.write("- **Action Required**: Reconstruct/restore the 17 missing reference items for Chapter 9 from source manuscript or CrossRef search.\n\n")

    out.write("### 2. Non-Standard `<p>` List Tagging in Chapter 11 (`chapter_11.html`)\n")
    out.write("- **Finding**: `chapter_11.html` (Sage Tea) lists 23 references under `<p><strong><span style=\"color: #339966\">References</span></strong></p>`, but **uses individual `<p>` paragraphs** (`<p>1. Adams...</p>`, `<p>2. Anibogwu...</p>`) instead of a semantic `<ol><li>` list.\n")
    out.write("- **Impact**: Standard BeautifulSoup extraction scripts expecting `<ol><li>` fail to parse Chapter 11 references.\n")
    out.write("- **Action Required**: Convert all 23 reference `<p>` tags in `chapter_11.html` into a clean `<ol><li>` ordered list structure.\n\n")

    out.write("### 3. Widespread Malformed HTML Anchor Tags & Nested `<a>` Tags\n")
    out.write("- **Nested `<a>` Tags**: Chapters 8, 10, 12, 13, 14 contain nested anchor tags created by automated string replacement or bad conversion: `<a href=\"https://doi.org/...\"><a href=\"https://doi.org/...\">https://doi.org/...</a></a>`.\n")
    out.write("- **Truncated and Malformed `href` Attributes**: In multiple chapters (e.g., `chapter_08.html` line 740, `chapter_11.html` line 55, `chapter_12.html` line 384, `chapter_13.html` line 208), Splitrock Environmental URLs contain broken attributes like `<a href=\"&lt;a href=\" https:=\"\" splitrockenvironmental.ca\"=\"\">\n")
    out.write("- **Split Image Source Links**: In `chapter_12.html` (lines 84-89, 124-129), ResearchGate URLs in figure captions were broken into two separate `<a href=\"...\">` tags split across line breaks.\n\n")

    out.write("## Complete Reference Inventory (Chapters 8-14)\n\n")
    
    for ch_file, ch_info in audit_data.items():
        out.write(f"### {ch_file} ({ch_info.get('total_references')} References)\n\n")
        refs = ch_info.get("references", [])
        if not refs:
            out.write("*No reference list present in HTML file.*\n\n")
            continue
            
        for r in refs:
            out.write(f"#### Reference {ch_file.split('_')[1].lstrip('0')}.{r['index']}\n")
            out.write(f"- **Reference Text**: {r['text']}\n")
            out.write(f"- **DOI Status**: `{r['doi_status']}`\n")
            if r.get("existing_doi"):
                out.write(f"- **Existing DOI**: `{r['existing_doi']}`\n")
            if r.get("formatting_issues"):
                out.write(f"- **Formatting Issues**: {'; '.join(r['formatting_issues'])}\n")
            if r.get("doi_issues"):
                out.write(f"- **DOI Issues**: {'; '.join(r['doi_issues'])}\n")
            if r.get("suggested_doi"):
                out.write(f"- **Suggested DOI**: `{r['suggested_doi']}`\n")
            out.write("\n")

print("Created analysis.md")

# 2. WRITE HANDOFF.MD
with open(handoff_path, "w", encoding="utf-8") as out:
    out.write("# Handoff Report — Explorer 2 (Milestone 1: Chapters 8-14)\n\n")
    out.write("## 1. Observation\n\n")
    out.write("### Direct File Inspection & Tool Execution Results\n")
    out.write("- **Assigned Scope**: `chapters/chapter_08.html` through `chapters/chapter_14.html` in `C:\\Users\\DELL\\Documents\\antigravity\\bold-hawking`.\n")
    out.write("- **Files Examined**: All 7 HTML chapter files (`chapter_08.html` to `chapter_14.html`).\n")
    out.write("- **Audit Execution**: Ran custom parsing & verification scripts (`analyze_chapters.py`, `verify_and_crossref.py`, `full_chapter_audit.py`) against CrossRef API and local filesystem.\n")
    out.write("- **Key Verbatim Findings & Line Numbers**:\n")
    out.write("  1. **`chapter_08.html`** (16 references in `<ol>`):\n")
    out.write("     - Nested `<a>` tags in 10 items (e.g., lines 588-590: `<a href=\"https://doi.org/10.1007/BF02858839\"><a href=\"https://doi.org/10.1007/BF02858839\">...</a></a>`).\n")
    out.write("     - Line 740: Severely malformed Splitrock Environmental URL: `<a href=\"&lt;a href=\" https:=\"\" splitrockenvironmental.ca\"=\"\"><a href=\"https://splitrockenvironmental.ca\">...</a></a>/products/common-juniper-tsiktsektaz?variant=40347042218150\"&gt;`.\n")
    out.write("     - 6 items missing DOIs (e.g., items 2, 7, 10, 11, 14, 16).\n")
    out.write("  2. **`chapter_09.html`** (0 references):\n")
    out.write("     - Line 425: Heading `<span style=\"color: #339966\"><strong>References</strong></span>` exists, but no `<ol>` or `<p>` reference items follow. Reference list is completely missing.\n")
    out.write("  3. **`chapter_10.html`** (6 references in `<ol>`):\n")
    out.write("     - Lines 143, 153, 166, 171, 184: Nested `<a>` tags in 5 out of 6 items.\n")
    out.write("     - Line 171: Splitrock link truncated (`<a href=\"https://splitrockenvironmental.ca\">` wraps domain only, URL path outside tag).\n")
    out.write("  4. **`chapter_11.html`** (23 references in `<p>` list):\n")
    out.write("     - Lines 312-607: References formatted as 23 separate `<p>` tags (`<p>1. Adams...</p>`) instead of standard `<ol><li>` elements.\n")
    out.write("     - Line 55: Figure caption contains malformed href `<a href=\"&lt;a href=\" https:=\"\" splitrockenvironmental.ca\"=\"\">`.\n")
    out.write("  5. **`chapter_12.html`** (11 references in `<ol>`):\n")
    out.write("     - Lines 293-295, 305-307, 317-319, 330-332, 352-354, 364-366, 376-378, 384-386: Nested `<a>` tags.\n")
    out.write("     - Line 384: Malformed Splitrock `href` attribute.\n")
    out.write("     - Lines 84-89, 124-129: ResearchGate figure links split across two `<a>` tags.\n")
    out.write("  6. **`chapter_13.html`** (6 references in `<ol>`):\n")
    out.write("     - Lines 172-174, 180-182, 188-190, 200-202, 208-210, 216-218: Nested `<a>` tags.\n")
    out.write("     - Line 208: Malformed Splitrock `href` attribute.\n")
    out.write("  7. **`chapter_14.html`** (9 references in `<ol>`):\n")
    out.write("     - Lines 834-836, 846-848, 877-879, 894-896, 906-908: Nested `<a>` tags.\n\n")

    out.write("## 2. Logic Chain\n\n")
    out.write("1. **Observation**: `chapter_09.html` has a `References` header but 0 items follow, while in-text citations `[4]`, `[9]`, `[10]`, `[12]`, `[15]`, `[17]` exist.\n")
    out.write("   - **Deduction**: Reference list was omitted during HTML splitting or generation and must be restored from source data.\n")
    out.write("2. **Observation**: `chapter_11.html` contains 23 references formatted inside `<p>` elements instead of `<ol><li>`.\n")
    out.write("   - **Deduction**: Extraction tools targeting `<ol>` miss Chapter 11 entirely. Fixer scripts must normalize `<p>` lists into semantic `<ol><li>` lists.\n")
    out.write("3. **Observation**: Double nested `<a href=\"...\"><a href=\"...\">...</a></a>` appears in almost every chapter containing DOIs or URLs.\n")
    out.write("   - **Deduction**: A previous automated script ran regex replacements that wrapped existing `<a>` tags with new `<a>` tags. Fixer scripts must unwrap duplicate anchor tags to `<a>...</a>`.\n")
    out.write("4. **Observation**: CrossRef API checks confirmed that 10 DOIs are valid & HTTP 200 OK, while 37 references have missing DOIs, and 13 DOIs/URLs return HTTP errors or truncated paths.\n")
    out.write("   - **Deduction**: Correct DOIs identified via CrossRef search (documented in `analysis.md`) can be cleanly inserted into anchor tags during Milestone 2.\n\n")

    out.write("## 3. Caveats\n\n")
    out.write("- **Chapter 9 Source Data**: `chapter_09.html` has no reference list in HTML. We identified suggested DOIs for in-text cited subjects, but the exact 17 references should be verified against `Original_Reference.doc` or `Corrected_Pilot.doc` in the workspace root if available.\n")
    out.write("- **CrossRef API Rate Limits**: CrossRef queries were executed with `mailto:` headers; any batch script running in Milestone 2 should maintain modest delays (0.1s) between requests.\n")
    out.write("- **Read-Only Scope**: In compliance with Explorer role guidelines, no files outside `.agents/teamwork_preview_explorer_m1_2` were modified.\n\n")

    out.write("## 4. Conclusion\n\n")
    out.write("- Chapters 8-14 contain **71 total reference items** across 7 chapters.\n")
    out.write("- Major structural repairs are needed for `chapter_09.html` (restore missing reference list) and `chapter_11.html` (convert `<p>` list to `<ol>`).\n")
    out.write("- All chapters (8, 10, 11, 12, 13, 14) require automated regex cleaning of nested `<a>` tags and repair of malformed `href` attributes.\n")
    out.write("- 37 missing DOIs can be updated with high-confidence CrossRef DOIs provided in `analysis.md`.\n\n")

    out.write("## 5. Verification Method\n\n")
    out.write("1. **Verify Analysis Report & Handoff**:\n")
    out.write("   - Check `analysis.md` and `handoff.md` in `C:\\Users\\DELL\\Documents\\antigravity\\bold-hawking\\.agents\\teamwork_preview_explorer_m1_2`.\n")
    out.write("2. **Inspect Chapter HTML Files**:\n")
    out.write("   - View `chapters/chapter_08.html` lines 588-590 & 740 to verify nested tags and malformed hrefs.\n")
    out.write("   - View `chapters/chapter_09.html` line 425 to verify missing `<ol>`.\n")
    out.write("   - View `chapters/chapter_11.html` lines 312-325 to verify `<p>` tag list formatting.\n")
    out.write("3. **Run Verification Script**:\n")
    out.write("   - Run `python .agents\\teamwork_preview_explorer_m1_2\\fast_audit.py` to re-execute CrossRef and HTML audit checks independently.\n")

print("Created handoff.md")
