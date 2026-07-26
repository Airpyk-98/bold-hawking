import json
import re

with open('.agents/teamwork_preview_explorer_m1_1/inventory_ch1_7.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

with open('.agents/teamwork_preview_explorer_m1_1/m1_detailed_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

# Build a map of audit data by chapter filename
audit_map = {ch['chapter_filename']: ch for ch in audit}

final_report = []

for ch in inventory:
    ch_file = ch['file']
    ch_num = int(ch_file.replace('chapter_', '').replace('.html', ''))
    title = ch['title']
    
    aud_ch = audit_map.get(ch_file, {})
    
    # Analyze chapter level issues
    ref_count = ch['ref_count']
    nested_a_count = 0
    plain_doi_count = 0
    missing_doi_count = 0
    broken_doi_count = 0
    hallucinated_doi_count = 0
    
    processed_refs = []
    
    for ref in ch['references']:
        ref_num = ref['ref_num']
        full_text = ref['full_text']
        raw_html = ref['raw_html']
        
        has_nested = ref['has_nested_a']
        if has_nested:
            nested_a_count += 1
            
        plain_dois = ref['plain_dois']
        if plain_dois:
            plain_doi_count += 1
            
        all_dois = ref['all_dois']
        if not all_dois:
            missing_doi_count += 1
            
        # Match with audit data
        matching_aud_ref = None
        if aud_ch.get('references'):
            for ar in aud_ch['references']:
                if ar['ref_num'] == ref_num:
                    matching_aud_ref = ar
                    break
        
        doi_details = []
        if matching_aud_ref:
            for d in matching_aud_ref.get('doi_audit', []):
                extracted = d['extracted_doi']
                status = d['http_status']
                err = d.get('http_error')
                crossref = d.get('crossref_match')
                
                is_404 = (status == 404)
                if is_404:
                    broken_doi_count += 1
                
                # Check for title match / hallucinated DOI
                suggested_doi = None
                top_match_title = None
                if crossref and isinstance(crossref, list) and len(crossref) > 0:
                    top = crossref[0]
                    suggested_doi = top.get('doi')
                    top_match_title = top.get('title')
                    
                    if is_404 or (suggested_doi and suggested_doi.lower() != extracted.lower() and top.get('score', 0) > 60):
                        hallucinated_doi_count += 1
                
                doi_details.append({
                    "extracted_doi": extracted,
                    "http_status": status,
                    "http_error": err,
                    "is_404": is_404,
                    "suggested_doi": suggested_doi,
                    "top_match_title": top_match_title
                })
        
        processed_refs.append({
            "ref_num": ref_num,
            "authors": ref['authors'],
            "year": ref['year'],
            "title": ref['title'],
            "full_text": full_text,
            "raw_html": raw_html,
            "has_nested_a": has_nested,
            "all_dois": all_dois,
            "plain_dois": plain_dois,
            "doi_details": doi_details
        })
        
    final_report.append({
        "chapter_file": ch_file,
        "chapter_number": ch_num,
        "title": title,
        "total_references": ref_count,
        "nested_a_count": nested_a_count,
        "plain_doi_count": plain_doi_count,
        "missing_doi_count": missing_doi_count,
        "broken_doi_404_count": broken_doi_count,
        "hallucinated_doi_count": hallucinated_doi_count,
        "references": processed_refs
    })

out_json = r".agents\teamwork_preview_explorer_m1_1\final_summary_ch1_7.json"
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(final_report, f, indent=2, ensure_ascii=False)

print(f"Final combined summary saved to {out_json}")
