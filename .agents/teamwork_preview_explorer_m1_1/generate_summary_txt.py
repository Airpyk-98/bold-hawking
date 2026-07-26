import json

with open(r'.agents\teamwork_preview_explorer_m1_1\local_analysis.json', 'r', encoding='utf-8') as f:
    chapters = json.load(f)

out_text_lines = []

out_text_lines.append("SUMMARY OF CHAPTERS 1 - 7:")
out_text_lines.append("=" * 60)

for ch in chapters:
    out_text_lines.append(f"Chapter File: {ch['file']}")
    out_text_lines.append(f"  Title: {ch['h1_title']}")
    out_text_lines.append(f"  Reference Headings: {ch['ref_headings']}")
    out_text_lines.append(f"  Total OLs in doc: {ch['ol_summary']}")
    out_text_lines.append(f"  Total References Count: {ch['ref_count']}")
    
    nested_a_cnt = sum(1 for r in ch['references'] if r['has_nested_a'])
    plain_doi_cnt = sum(1 for r in ch['references'] if len(r['plain_dois']) > 0)
    no_doi_cnt = sum(1 for r in ch['references'] if len(r['all_dois']) == 0)
    
    out_text_lines.append(f"  - References with Nested <a> tags: {nested_a_cnt}")
    out_text_lines.append(f"  - References with Plain Text DOIs (unlinked): {plain_doi_cnt}")
    out_text_lines.append(f"  - References with NO DOIs: {no_doi_cnt}")
    
    for ref in ch['references']:
        issues = []
        if ref['has_nested_a']:
            issues.append("NESTED_A_TAGS")
        if ref['plain_dois']:
            issues.append(f"PLAIN_TEXT_DOI:{ref['plain_dois']}")
        if not ref['apa_structured']:
            issues.append("NON_STANDARD_APA_FORMAT")
        if not ref['all_dois']:
            issues.append("MISSING_DOI")
            
        out_text_lines.append(f"    Ref #{ref['ref_num']}: {ref['text'][:90]}...")
        if issues:
            out_text_lines.append(f"      [ISSUES]: {', '.join(issues)}")
        out_text_lines.append(f"      [Anchors Count]: {ref['a_count']}, [DOIs Found]: {ref['all_dois']}")
    out_text_lines.append("-" * 60)

with open(r'.agents\teamwork_preview_explorer_m1_1\summary_ch1_7.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out_text_lines))

print("Summary written to summary_ch1_7.txt")
