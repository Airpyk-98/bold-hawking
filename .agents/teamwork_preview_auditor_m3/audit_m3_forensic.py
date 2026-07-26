import os
import sys
import re
import json
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
OUTPUT_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_auditor_m3"

def string_similarity(a, b):
    if not a or not b:
        return 0.0
    a_clean = re.sub(r'[^\w\s]', '', a.lower()).strip()
    b_clean = re.sub(r'[^\w\s]', '', b.lower()).strip()
    return SequenceMatcher(None, a_clean, b_clean).ratio()

def check_html_cleanliness(filepath, content, soup):
    issues = []
    
    # 1. Check for nested <a> tags using regex and BeautifulSoup
    nested_a_regex = re.compile(r'<a\b[^>]*>(?:(?!</a>).)*?<a\b', re.IGNORECASE | re.DOTALL)
    if nested_a_regex.search(content):
        issues.append("Nested <a> tag detected via regex pattern")
    
    for a in soup.find_all('a'):
        if a.find('a'):
            issues.append(f"Nested <a> tag inside link: {a}")
            
    # 2. Check for malformed href attributes (e.g., href="https://doi.org/..."" or quotes issues)
    malformed_hrefs = re.findall(r'href=["\'](https?://doi\.org/[^"\'>\s]+)["\']\s*["\']', content)
    if malformed_hrefs:
        issues.append(f"Malformed double-quoted href detected: {malformed_hrefs}")
        
    # Check for empty href or href="#"
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href == '' or href == '#':
            issues.append(f"Empty or placeholder href attribute: {a}")
            
    # Check for unclosed <a> tags
    open_a_count = len(re.findall(r'<a\b', content, re.IGNORECASE))
    close_a_count = len(re.findall(r'</a>', content, re.IGNORECASE))
    if open_a_count != close_a_count:
        issues.append(f"Mismatched <a> tag count: <a count={open_a_count}, </a> count={close_a_count}")
        
    return issues

def query_crossref_api(doi):
    if not doi:
        return {'status': None, 'error': 'No DOI'}
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
    doi_clean = re.sub(r'[\.\,\;\>\)\]]+$', '', doi_clean)
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ForensicAuditor/1.0 (mailto:audit@example.com)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                msg = data.get('message', {})
                titles = msg.get('title', [])
                title = titles[0] if titles else ""
                container = msg.get('container-title', [])
                journal = container[0] if container else ""
                year = None
                published = msg.get('published-print') or msg.get('published-online') or msg.get('issued')
                if published and 'date-parts' in published and published['date-parts']:
                    year = published['date-parts'][0][0]
                return {
                    'status': 200,
                    'doi': msg.get('DOI', doi_clean),
                    'title': title,
                    'journal': journal,
                    'year': year,
                    'raw_msg': msg
                }
    except urllib.error.HTTPError as e:
        return {'status': e.code, 'error': f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {'status': 500, 'error': str(e)}
    return {'status': 404, 'error': 'Not found'}

def verify_doi_http(doi):
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
    doi_clean = re.sub(r'[\.\,\;\>\)\]]+$', '', doi_clean)
    url = f"https://doi.org/{doi_clean}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {'status': resp.status, 'final_url': resp.url}
    except urllib.error.HTTPError as e:
        return {'status': e.code, 'final_url': None, 'error': str(e)}
    except Exception as e:
        return {'status': 500, 'final_url': None, 'error': str(e)}

def extract_chapter_references(ch_num):
    filepath = os.path.join(CHAPTER_DIR, f"chapter_{ch_num:02d}.html")
    if not os.path.exists(filepath):
        return [], [f"File chapter_{ch_num:02d}.html missing"]
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    html_issues = check_html_cleanliness(filepath, content, soup)
    
    # Locate references block
    # References section can be <ol class="references">, <div class="references">, or heading with "References"
    ref_container = soup.find(class_=re.compile(r'references', re.I)) or soup.find(id=re.compile(r'references', re.I))
    
    items = []
    if ref_container:
        items = ref_container.find_all(['li', 'p'])
    else:
        # Look for headers containing References
        ref_heading = soup.find(lambda tag: tag.name in ['h2', 'h3', 'h4'] and 'reference' in tag.get_text().lower())
        if ref_heading:
            parent = ref_heading.parent
            # find ol or ul or list items after heading
            next_ol = ref_heading.find_next(['ol', 'ul'])
            if next_ol:
                items = next_ol.find_all('li')
            else:
                curr = ref_heading.next_sibling
                while curr:
                    if getattr(curr, 'name', None) in ['p', 'li']:
                        items.append(curr)
                    curr = curr.next_sibling
        else:
            # Fallback to last <ol>
            ols = soup.find_all('ol')
            if ols:
                items = ols[-1].find_all('li')
                
    refs = []
    for idx, item in enumerate(items, 1):
        item_text = item.get_text().strip()
        if not item_text or len(item_text) < 10:
            continue
            
        links = []
        for a in item.find_all('a'):
            href = a.get('href', '')
            text = a.get_text().strip()
            links.append({'href': href, 'text': text, 'raw': str(a)})
            
        # Extract DOIs from hrefs and text
        dois_href = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', " ".join([l['href'] for l in links]))
        dois_text = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', item_text)
        
        all_dois = []
        for d in dois_href + dois_text:
            d_clean = re.sub(r'[\.\,\;\>\)\]]+$', '', d).strip()
            if d_clean and d_clean not in all_dois:
                all_dois.append(d_clean)
                
        refs.append({
            'chapter': ch_num,
            'ref_num': idx,
            'text': item_text,
            'links': links,
            'dois': all_dois,
            'html': str(item)
        })
        
    return refs, html_issues

def audit_single_doi(doi, ref_text):
    crossref_info = query_crossref_api(doi)
    http_info = verify_doi_http(doi)
    
    crossref_title = crossref_info.get('title', '')
    sim_score = string_similarity(ref_text, crossref_title) if crossref_title else 0.0
    
    return {
        'doi': doi,
        'http_status': http_info.get('status'),
        'final_url': http_info.get('final_url'),
        'crossref_status': crossref_info.get('status'),
        'crossref_title': crossref_title,
        'crossref_journal': crossref_info.get('journal'),
        'crossref_year': crossref_info.get('year'),
        'title_similarity': sim_score,
        'error': crossref_info.get('error') or http_info.get('error')
    }

def run_full_m3_audit():
    print("=== STARTING MILESTONE 3 FORENSIC INTEGRITY AUDIT (CHAPTERS 1-20) ===")
    
    all_ch_results = {}
    total_refs = 0
    total_dois = 0
    total_html_issues = 0
    
    chapter_html_issues = {}
    chapter_doi_audits = {}
    
    # Step 1: Extract all references & check HTML
    for ch in range(1, 21):
        refs, html_issues = extract_chapter_references(ch)
        chapter_html_issues[ch] = html_issues
        total_html_issues += len(html_issues)
        
        print(f"Chapter {ch:02d}: Extracted {len(refs)} references. HTML Issues: {len(html_issues)}")
        if html_issues:
            for iss in html_issues:
                print(f"   [HTML ISSUE] Ch{ch:02d}: {iss}")
                
        all_ch_results[ch] = refs
        total_refs += len(refs)
        for r in refs:
            total_dois += len(r['dois'])
            
    print(f"\nTotal References Extracted across Ch 1-20: {total_refs}")
    print(f"Total DOIs Extracted: {total_dois}")
    print(f"Total HTML Structure Issues: {total_html_issues}\n")
    
    # Step 2: Audit all DOIs in parallel
    doi_tasks = []
    for ch, refs in all_ch_results.items():
        for r in refs:
            for doi in r['dois']:
                doi_tasks.append((ch, r['ref_num'], r['text'], doi))
                
    print(f"Verifying {len(doi_tasks)} DOIs via HTTP & CrossRef API...")
    
    audited_dois = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_task = {
            executor.submit(audit_single_doi, doi, text): (ch, rnum, text, doi)
            for (ch, rnum, text, doi) in doi_tasks
        }
        
        completed = 0
        for future in as_completed(future_to_task):
            ch, rnum, text, doi = future_to_task[future]
            try:
                res = future.result()
                res['chapter'] = ch
                res['ref_num'] = rnum
                res['ref_text'] = text
                audited_dois.append(res)
            except Exception as e:
                audited_dois.append({
                    'chapter': ch,
                    'ref_num': rnum,
                    'ref_text': text,
                    'doi': doi,
                    'http_status': 500,
                    'crossref_status': 500,
                    'error': str(e),
                    'title_similarity': 0.0
                })
            completed += 1
            if completed % 10 == 0 or completed == len(doi_tasks):
                print(f"Progress: {completed}/{len(doi_tasks)} DOIs audited.")
                
    # Step 3: Analyze findings & violations
    violations = []
    warnings = []
    clean_dois_count = 0
    
    for item in audited_dois:
        ch = item['chapter']
        rnum = item['ref_num']
        doi = item['doi']
        http_st = item['http_status']
        cr_st = item['crossref_status']
        sim = item['title_similarity']
        cr_title = item.get('crossref_title', '')
        text = item['ref_text']
        
        # Check 1: HTTP 200 OK
        if http_st != 200 and cr_st != 200:
            violations.append({
                'type': 'BROKEN_DOI',
                'chapter': ch,
                'ref_num': rnum,
                'doi': doi,
                'http_status': http_st,
                'crossref_status': cr_st,
                'details': f"DOI {doi} failed resolution (HTTP status: {http_st}, CrossRef: {cr_st}, error: {item.get('error')})"
            })
        elif sim < 0.25 and cr_title:
            # Check 2: Hallucinated / Mismatched DOI
            violations.append({
                'type': 'HALLUCINATED_DOI_MISMATCH',
                'chapter': ch,
                'ref_num': rnum,
                'doi': doi,
                'title_similarity': sim,
                'ref_text': text[:100],
                'crossref_title': cr_title,
                'details': f"DOI {doi} resolves to paper '{cr_title}' which does NOT match reference text '{text[:80]}...' (similarity: {sim:.2f})"
            })
        elif sim < 0.50 and cr_title:
            warnings.append({
                'type': 'LOW_TITLE_SIMILARITY',
                'chapter': ch,
                'ref_num': rnum,
                'doi': doi,
                'title_similarity': sim,
                'ref_text': text[:100],
                'crossref_title': cr_title
            })
        else:
            clean_dois_count += 1

    # Check 3: Check refs missing DOI
    refs_without_doi = []
    for ch, refs in all_ch_results.items():
        for r in refs:
            if not r['dois']:
                refs_without_doi.append({
                    'chapter': ch,
                    'ref_num': r['ref_num'],
                    'text': r['text']
                })

    # Compile Final Report Data
    report_data = {
        'total_chapters': 20,
        'total_references': total_refs,
        'total_dois': total_dois,
        'total_html_issues': total_html_issues,
        'clean_dois_count': clean_dois_count,
        'violations': violations,
        'warnings': warnings,
        'html_issues_by_chapter': chapter_html_issues,
        'refs_without_doi': refs_without_doi,
        'audited_dois_detail': audited_dois
    }
    
    with open(os.path.join(OUTPUT_DIR, "audit_results_m3.json"), 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
        
    print("\n=================== AUDIT SUMMARY ===================")
    print(f"Total References: {total_refs}")
    print(f"Total DOIs Checked: {total_dois}")
    print(f"HTML Issues Count: {total_html_issues}")
    print(f"Clean Verified DOIs: {clean_dois_count}")
    print(f"VIOLATIONS FOUND: {len(violations)}")
    print(f"WARNINGS FOUND: {len(warnings)}")
    print(f"REFS WITHOUT DOI: {len(refs_without_doi)}")
    print("=====================================================\n")
    
    if len(violations) > 0 or total_html_issues > 0:
        print("VERDICT: INTEGRITY VIOLATION")
    else:
        print("VERDICT: CLEAN")

if __name__ == '__main__':
    run_full_m3_audit()
