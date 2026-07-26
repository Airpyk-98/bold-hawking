import json

with open('.agents/teamwork_preview_explorer_m1_1/final_summary_ch1_7.json', 'r', encoding='utf-8') as f:
    chapters = json.load(f)

print("CHAPTER   | REFS | NESTED <a> | MISSING DOI | BROKEN (404) DOI")
print("-" * 62)
tot_refs = 0
tot_nested = 0
tot_missing = 0
tot_broken = 0

for ch in chapters:
    r_cnt = ch['total_references']
    n_cnt = ch['nested_a_count']
    m_cnt = ch['missing_doi_count']
    b_cnt = ch['broken_doi_404_count']
    tot_refs += r_cnt
    tot_nested += n_cnt
    tot_missing += m_cnt
    tot_broken += b_cnt
    print(f"{ch['chapter_file']:<9} | {r_cnt:<4} | {n_cnt:<10} | {m_cnt:<11} | {b_cnt:<16}")

print("-" * 62)
print(f"TOTAL     | {tot_refs:<4} | {tot_nested:<10} | {tot_missing:<11} | {tot_broken:<16}")
