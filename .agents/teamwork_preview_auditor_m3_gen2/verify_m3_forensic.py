import os
import sys
import re
import json
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

CHAPTER_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
GEN1_RESULTS = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_auditor_m3\audit_results_m3.json"
OUTPUT_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_auditor_m3_gen2"

def string_similarity(a, b):
    if not a or not b:
        return 0.0
    a_clean = re.sub(r'[^\w\s]', '', a.lower()).strip()
    b_clean = re.sub(r'[^\w\s]', '', b.lower()).strip()
    return SequenceMatcher(None, a_clean, b_clean).ratio()

def audit_html_cleanliness(content, soup):
    issues = []
    
    # 1. Stray prefix links: <a href="https://doi.org/">https://doi.org/</a>
    stray_prefixes = re.findall(r'<a\s+href=["\']https?://doi\.org/?["\']>\s*https?://doi\.org/?\s*</a>', content, re.I)
    if stray_prefixes:
        issues.append(f"Stray/broken prefix link: {stray_prefixes}")
        
    # 2. Nested <a> tags
    for a in soup.find_all('a'):
        if a.find('a'):
            issues.append(f"Nested <a> tag inside link: {a}")
            
    # 3. Unclosed / mismatched <a> tags
    open_a_count = len(re.findall(r'<a\b', content, re.I))
    close_a_count = len(re.findall(r'</a>', content, re.I))
    if open_a_count != close_a_count:
        issues.append(f"Mismatched <a> count: <a={open_a_count}, </a>={close_a_count}")
        
    # 4. Malformed hrefs (e.g. quotes issues, placeholder hrefs)
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href == '' or href == '#':
            issues.append(f"Empty or placeholder href attribute: {a}")
            
    # 5. Plaintext unhyperlinked DOIs (DOI text in reference not enclosed in <a> tag)
    for li in soup.find_all('li'):
        text = li.get_text()
        dois_in_text = re.findall(r'https?://doi\.org/10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
        linked_hrefs = [a.get('href', '') for a in li.find_all('a')]
        for d in dois_in_text:
            d_clean = d.strip()
            if not any(d_clean in href for href in linked_hrefs):
                issues.append(f"Unhyperlinked plain text DOI in <li>: {d_clean}")

    return issues

def main():
    print("=== MILESTONE 3 FORENSIC INTEGRITY AUDIT (CHAPTERS 1 - 20) ===")
    
    # Load Gen 1 results for CrossRef title matching if available
    gen1_data = {}
    if os.path.exists(GEN1_RESULTS):
        with open(GEN1_RESULTS, 'r', encoding='utf-8') as f:
            gen1_data = json.load(f)
            
    audited_dois_lookup = {}
    if 'audited_dois_detail' in gen1_data:
        for item in gen1_data['audited_dois_detail']:
            key = (item['chapter'], item['ref_num'], item['doi'])
            audited_dois_lookup[key] = item
            
    total_chapters = 20
    total_references = 0
    total_dois = 0
    all_html_issues = {}
    all_violations = []
    all_warnings = []
    chapter_summaries = {}
    
    for ch in range(1, 21):
        filepath = os.path.join(CHAPTER_DIR, f"chapter_{ch:02d}.html")
        if not os.path.exists(filepath):
            print(f"Chapter {ch:02d}: File missing!")
            continue
            
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check HTML cleanliness
        html_issues = audit_html_cleanliness(content, soup)
        if html_issues:
            all_html_issues[ch] = html_issues
            
        # Extract references
        # Find references section
        ref_section = soup.find(id=re.compile(r'references', re.I)) or soup.find(class_=re.compile(r'references', re.I))
        items = []
        if ref_section:
            items = ref_section.find_all('li')
        else:
            ref_heading = soup.find(lambda tag: tag.name in ['h2', 'h3', 'h4'] and 'reference' in tag.get_text().lower())
            if ref_heading:
                next_ol = ref_heading.find_next(['ol', 'ul'])
                if next_ol:
                    items = next_ol.find_all('li')
            if not items:
                ols = soup.find_all('ol')
                if ols:
                    items = ols[-1].find_all('li')
                    
        total_references += len(items)
        ch_dois = 0
        ch_violations = []
        ch_warnings = []
        
        for idx, item in enumerate(items, 1):
            text = item.get_text().strip()
            links = item.find_all('a')
            
            # Find DOIs
            dois = []
            for a in links:
                href = a.get('href', '')
                d_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', href)
                if d_match:
                    d_clean = re.sub(r'[\.\,\;\>\)\]]+$', '', d_match.group(0))
                    if d_clean not in dois:
                        dois.append(d_clean)
            
            # Also check text for DOIs
            text_dois = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
            for td in text_dois:
                td_clean = re.sub(r'[\.\,\;\>\)\]]+$', '', td)
                if td_clean not in dois:
                    dois.append(td_clean)
                    
            ch_dois += len(dois)
            total_dois += len(dois)
            
            # Check DOIs against audit lookup
            for doi in dois:
                key = (ch, idx, doi)
                if key in audited_dois_lookup:
                    audit_rec = audited_dois_lookup[key]
                    http_st = audit_rec.get('http_status')
                    cr_st = audit_rec.get('crossref_status')
                    sim = audit_rec.get('title_similarity', 0.0)
                    cr_title = audit_rec.get('crossref_title', '')
                    
                    if http_st != 200 and cr_st != 200:
                        v = {
                            'type': 'BROKEN_DOI',
                            'chapter': ch,
                            'ref_num': idx,
                            'doi': doi,
                            'http_status': http_st,
                            'crossref_status': cr_st,
                            'error': audit_rec.get('error'),
                            'details': f"DOI {doi} failed resolution (HTTP: {http_st}, CrossRef: {cr_st})"
                        }
                        ch_violations.append(v)
                        all_violations.append(v)
                    elif sim < 0.25 and cr_title:
                        v = {
                            'type': 'HALLUCINATED_DOI_MISMATCH',
                            'chapter': ch,
                            'ref_num': idx,
                            'doi': doi,
                            'similarity': sim,
                            'ref_text': text[:120],
                            'crossref_title': cr_title,
                            'details': f"DOI {doi} points to '{cr_title}' which does not match cited paper '{text[:80]}...'"
                        }
                        ch_violations.append(v)
                        all_violations.append(v)
                    elif sim < 0.50 and cr_title:
                        w = {
                            'type': 'LOW_TITLE_SIMILARITY',
                            'chapter': ch,
                            'ref_num': idx,
                            'doi': doi,
                            'similarity': sim,
                            'ref_text': text[:120],
                            'crossref_title': cr_title
                        }
                        ch_warnings.append(w)
                        all_warnings.append(w)
                        
        chapter_summaries[ch] = {
            'ref_count': len(items),
            'doi_count': ch_dois,
            'html_issues_count': len(html_issues),
            'violations_count': len(ch_violations),
            'warnings_count': len(ch_warnings)
        }

    verdict = "INTEGRITY VIOLATION" if (all_violations or all_html_issues) else "CLEAN"
    
    summary_report = {
        'verdict': verdict,
        'total_chapters': total_chapters,
        'total_references': total_references,
        'total_dois': total_dois,
        'total_html_issues': sum(len(v) for v in all_html_issues.values()),
        'total_violations': len(all_violations),
        'total_warnings': len(all_warnings),
        'html_issues_by_chapter': all_html_issues,
        'violations': all_violations,
        'warnings': all_warnings,
        'chapter_summaries': chapter_summaries
    }
    
    out_file = os.path.join(OUTPUT_DIR, "forensic_audit_report.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, indent=2, ensure_ascii=False)
        
    print(f"\n==========================================")
    print(f"VERDICT: {verdict}")
    print(f"Total References: {total_references}")
    print(f"Total DOIs: {total_dois}")
    print(f"Total HTML Structure Issues: {sum(len(v) for v in all_html_issues.values())}")
    print(f"Total Integrity Violations: {len(all_violations)}")
    print(f"Total Warnings: {len(all_warnings)}")
    print(f"Report saved to: {out_file}")
    print(f"==========================================\n")

if __name__ == '__main__':
    main()
