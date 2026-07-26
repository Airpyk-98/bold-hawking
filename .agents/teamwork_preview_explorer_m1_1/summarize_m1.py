import json

with open('.agents/teamwork_preview_explorer_m1_1/extracted_raw_m1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for ch in data:
    print(f"=== {ch['file']} === (Header: {ch['has_ref_header']}, OL: {ch['has_ol']}, Count: {len(ch['references'])})")
    for ref in ch['references']:
        print(f"  [{ref['ref_num']}] {ref['text'][:120]}")
        print(f"      Anchors: {ref['anchors']}")
        print(f"      DOIs: {ref['doi_matches']}")
        print(f"      URLs: {ref['url_matches']}")
        print()
