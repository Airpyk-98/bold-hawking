import json

with open(r'.agents\teamwork_preview_explorer_m1_1\local_analysis.json', 'r', encoding='utf-8') as f:
    chapters = json.load(f)

print("SUMMARY OF CHAPTERS 1 - 7:")
print("=" * 60)

for ch in chapters:
    print(f"Chapter File: {ch['file']}")
    print(f"  Title: {ch['h1_title']}")
    print(f"  Reference Headings: {ch['ref_headings']}")
    print(f"  Total OLs in doc: {ch['ol_summary']}")
    print(f"  Total References Count: {ch['ref_count']}")
    
    nested_a_cnt = sum(1 for r in ch['references'] if r['has_nested_a'])
    plain_doi_cnt = sum(1 for r in ch['references'] if len(r['plain_dois']) > 0)
    no_doi_cnt = sum(1 for r in ch['references'] if len(r['all_dois']) == 0)
    
    print(f"  - References with Nested <a> tags: {nested_a_cnt}")
    print(f"  - References with Plain Text DOIs (unlinked): {plain_doi_cnt}")
    print(f"  - References with NO DOIs: {no_doi_cnt}")
    
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
            
        print(f"    Ref #{ref['ref_num']}: {ref['text'][:90]}...")
        if issues:
            print(f"      [ISSUES]: {', '.join(issues)}")
        print(f"      [Anchors Count]: {ref['a_count']}, [DOIs Found]: {ref['all_dois']}")
    print("-" * 60)
