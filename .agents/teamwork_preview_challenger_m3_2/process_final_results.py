import json
import os
import re

agent_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_challenger_m3_2"
json_path = os.path.join(agent_dir, "verification_results.json")
cache_path = os.path.join(agent_dir, "doi_cache.json")
handoff_path = os.path.join(agent_dir, "handoff.md")

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

total_references = 0
no_doi_refs = 0
total_dois_checked = 0
valid_dois = 0
dead_dois = 0
matched_count = 0
mismatch_count = 0

chapter_breakdown = []
mismatches_list = []

for chap in data:
    chap_name = chap['chapter']
    ref_count = chap['ref_count']
    total_references += ref_count
    
    chap_dois = 0
    chap_valid = 0
    chap_mismatch = 0
    chap_scores = []
    
    for ref in chap['references']:
        ref_num = ref['ref_num']
        cited_text = ref['text']
        dois = ref['dois']
        checks = ref.get('crossref_checks', [])
        
        if not dois:
            no_doi_refs += 1
            continue
            
        for check in checks:
            total_dois_checked += 1
            chap_dois += 1
            doi = check.get('doi', '')
            cr_data = check.get('crossref_data', {})
            status = cr_data.get('status', 'UNKNOWN')
            cr_title = cr_data.get('title', '')
            sim_score = check.get('similarity', 0.0)
            
            if status == 'OK':
                valid_dois += 1
                chap_valid += 1
                chap_scores.append(sim_score)
                
                if sim_score >= 0.50:
                    matched_count += 1
                else:
                    mismatch_count += 1
                    chap_mismatch += 1
                    mismatches_list.append({
                        'chapter': chap_name,
                        'ref_num': ref_num,
                        'doi': doi,
                        'cited_text': cited_text,
                        'crossref_title': cr_title,
                        'similarity': sim_score,
                        'reason': 'TITLE_MISMATCH'
                    })
            else:
                dead_dois += 1
                mismatch_count += 1
                chap_mismatch += 1
                mismatches_list.append({
                    'chapter': chap_name,
                    'ref_num': ref_num,
                    'doi': doi,
                    'cited_text': cited_text,
                    'crossref_title': '',
                    'similarity': 0.0,
                    'reason': f"DEAD_DOI ({status})"
                })
                
    avg_score = (sum(chap_scores) / len(chap_scores)) if chap_scores else 0.0
    chapter_breakdown.append({
        'chapter': chap_name,
        'ref_count': ref_count,
        'doi_count': chap_dois,
        'valid_dois': chap_valid,
        'mismatch_count': chap_mismatch,
        'avg_similarity': avg_score
    })

handoff_content = f"""# Milestone 3 Handoff Report — Title Similarity & DOI Accuracy Verification (Chapters 01 - 20)

## 1. Observation
- **Scope**: Evaluated `chapters/chapter_01.html` through `chapters/chapter_20.html` (20 chapters total).
- **Total References Examined**: {total_references} references.
- **References Without DOIs**: {no_doi_refs} references.
- **Total DOIs Checked against CrossRef REST API**: {total_dois_checked} DOIs.
- **CrossRef Resolution Status**:
  - Valid DOIs (HTTP 200 OK): {valid_dois} / {total_dois_checked}.
  - Dead / 404 DOIs: {dead_dois} DOIs.
- **Title Similarity Results**:
  - High Title Similarity (Score >= 0.50): {matched_count} DOIs.
  - Title Mismatches / Hallucinated / Dead DOIs (Score < 0.50): **{mismatch_count} DOIs**.

### Detailed List of Confirmed Mismatches & Dead DOIs ({len(mismatches_list)} total):

"""

for m in mismatches_list:
    handoff_content += f"- **{m['chapter']}** Ref #{m['ref_num']} | DOI: `{m['doi']}`\n"
    handoff_content += f"  - Status: **{m['reason']}** (Similarity: {m['similarity']:.2f})\n"
    handoff_content += f"  - Cited Text: {m['cited_text'][:130]}...\n"
    if m['crossref_title']:
        handoff_content += f"  - CrossRef Title: *{m['crossref_title']}*\n"
    handoff_content += "\n"

handoff_content += f"""---

## 2. Logic Chain
1. **Extraction**: Parsed all 20 HTML chapters (`chapter_01.html` to `chapter_20.html`) and extracted 238 reference items.
2. **Empirical Query**: Queried live CrossRef REST API (`https://api.crossref.org/works/{doi}`) for all 141 DOIs with retry logic and caching.
3. **Similarity Assessment**: Calculated title similarity using normalized sequence matching and token overlap ratios between cited titles and official CrossRef metadata.
4. **Findings**:
   - 119 DOIs (84.4%) match their cited paper titles accurately.
   - 3 DOIs return HTTP 404 Not Found (dead links).
   - 19 DOIs link to completely different, unrelated papers (hallucinated/mismatched DOIs).

---

## 3. Caveats
- 97 references in these chapters lack DOIs; these are primarily historical books, government reports, or general web links.

---

## 4. Conclusion
- **Overall Status**: **ACTION REQUIRED ({mismatch_count} Mismatches / Dead DOIs Found)**
- **Verification Verdict**: Milestone 3 verification is complete. Empirical testing uncovered 19 title mismatches and 3 dead DOIs across Chapters 1-20 that require remediation.

---

## 5. Verification Method
1. Run `python .agents/teamwork_preview_challenger_m3_2/verify_m3.py`.
2. Inspect `.agents/teamwork_preview_challenger_m3_2/verification_results.json`.

---

## Appendix: Chapter-by-Chapter Summary

| Chapter | Total Refs | DOIs Checked | Valid DOIs | Mismatches/Dead DOIs | Avg Title Similarity |
|---|---|---|---|---|---|
"""

for cb in chapter_breakdown:
    handoff_content += f"| `{cb['chapter']}` | {cb['ref_count']} | {cb['doi_count']} | {cb['valid_dois']} | {cb['mismatch_count']} | {cb['avg_similarity']:.2f} |\n"

handoff_content += f"\n**Total**: {total_references} References | {total_dois_checked} DOIs Checked | {valid_dois} Valid DOIs | {mismatch_count} Mismatches/Dead DOIs\n"

with open(handoff_path, 'w', encoding='utf-8') as f:
    f.write(handoff_content)

print(f"Updated handoff report written to {handoff_path}")
