import json

with open('.agents/teamwork_preview_explorer_m1_1/m1_detailed_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for ch in data:
    print(f"=== {ch['chapter_filename']} ===")
    for ref in ch['references']:
        print(f"Ref #{ref['ref_num']}: Text: {ref['text'][:80]}...")
        print(f"   Nested A Tags: {ref['has_nested_a_tags']}")
        print(f"   Plain DOIs: {ref['has_plain_text_doi']}")
        for d_audit in ref['doi_audit']:
            status = d_audit['http_status']
            doi = d_audit['extracted_doi']
            err = d_audit.get('http_error')
            print(f"   DOI: {doi} -> Status: {status} ({err})")
            if d_audit.get('crossref_match') and isinstance(d_audit['crossref_match'], list):
                if d_audit['crossref_match']:
                    top = d_audit['crossref_match'][0]
                    print(f"     CrossRef Top Match DOI: {top['doi']} | Score: {top['score']}")
                    print(f"     CrossRef Title: {top['title']}")
    print()
