import os
import re
import sys
import json
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding='utf-8')

CACHE_FILE = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_challenger_m3_2\doi_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_tokens(text):
    cleaned = clean_text(text)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'for', 'with', 'by', 'at', 'to', 'from', 'is', 'are'}
    tokens = set(w for w in cleaned.split() if w not in stop_words and len(w) > 1)
    return tokens

def title_similarity(cr_title, ref_text, i_tags=None):
    if not cr_title or not ref_text:
        return 0.0
    
    cr_clean = clean_text(cr_title)
    ref_clean = clean_text(ref_text)
    
    ratio_full = SequenceMatcher(None, cr_clean, ref_clean).ratio()
    
    cr_tokens = get_tokens(cr_title)
    ref_tokens = get_tokens(ref_text)
    
    if not cr_tokens or not ref_tokens:
        overlap_score = 0.0
    else:
        intersection = cr_tokens.intersection(ref_tokens)
        overlap_score = len(intersection) / float(len(cr_tokens))
    
    itag_scores = []
    if i_tags:
        for itag in i_tags:
            itag_clean = clean_text(itag)
            itag_seq = SequenceMatcher(None, cr_clean, itag_clean).ratio()
            itag_tok = get_tokens(itag)
            if itag_tok and cr_tokens:
                itag_ov = len(cr_tokens.intersection(itag_tok)) / float(len(cr_tokens))
            else:
                itag_ov = 0.0
            itag_scores.append(max(itag_seq, itag_ov))
            
    max_itag = max(itag_scores) if itag_scores else 0.0
    return max(ratio_full, overlap_score, max_itag)

def extract_references_from_chapter(chap_path):
    if not os.path.exists(chap_path):
        return []
    with open(chap_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    ols = soup.find_all('ol')
    if not ols:
        return []
    
    ref_ol = ols[-1]
    references = []
    
    for idx, li in enumerate(ref_ol.find_all('li'), start=1):
        ref_text = li.get_text().strip()
        links = [a.get('href', '') for a in li.find_all('a') if a.get('href')]
        
        dois = []
        for link in links:
            m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', link)
            if m:
                d = m.group(0).rstrip('.')
                if d not in dois:
                    dois.append(d)
        
        raw_doi_m = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', ref_text)
        for d in raw_doi_m:
            d_clean = d.rstrip('.')
            if d_clean not in dois:
                dois.append(d_clean)
                
        i_tags = [i.get_text().strip() for i in li.find_all('i')]
        
        references.append({
            'ref_num': idx,
            'text': ref_text,
            'i_tags': i_tags,
            'links': links,
            'dois': dois
        })
        
    return references

def query_crossref_doi(doi, cache):
    doi_clean = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi)
    if doi_clean in cache:
        return cache[doi_clean]
    
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@antigravity.org'})
    
    result = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    item = data.get('message', {})
                    titles = item.get('title', [])
                    crossref_title = titles[0] if titles else ""
                    container_title = item.get('container-title', [""])[0] if item.get('container-title') else ""
                    authors = item.get('author', [])
                    result = {
                        'status': 'OK',
                        'doi': doi_clean,
                        'title': crossref_title,
                        'container': container_title,
                        'authors': authors
                    }
                    break
        except urllib.error.HTTPError as e:
            result = {'status': f'HTTP_{e.code}', 'doi': doi_clean, 'title': '', 'error': str(e)}
            if e.code == 404:
                break # 404 is definitive
        except Exception as e:
            result = {'status': 'ERROR', 'doi': doi_clean, 'title': '', 'error': str(e)}
        
        time.sleep(1.0 * (attempt + 1))
        
    if result:
        cache[doi_clean] = result
        save_cache(cache)
    time.sleep(0.2) # friendly rate limiting
    return result or {'status': 'ERROR', 'doi': doi_clean, 'title': '', 'error': 'Max retries exceeded'}

def main():
    base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
    chapters_dir = os.path.join(base_dir, "chapters")
    out_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_challenger_m3_2"
    
    cache = load_cache()
    all_results = []
    
    doi_count = 0
    valid_doi_count = 0
    matched_count = 0
    mismatched_count = 0
    http_error_count = 0
    no_doi_refs_count = 0
    
    summary_lines = []
    
    for i in range(1, 21):
        chap_name = f"chapter_{i:02d}.html"
        chap_path = os.path.join(chapters_dir, chap_name)
        refs = extract_references_from_chapter(chap_path)
        
        chap_result = {
            'chapter': chap_name,
            'ref_count': len(refs),
            'references': []
        }
        
        header_str = f"\n=== {chap_name} ({len(refs)} references) ==="
        print(header_str)
        summary_lines.append(header_str)
        
        for ref in refs:
            ref_info = {
                'ref_num': ref['ref_num'],
                'text': ref['text'],
                'dois': ref['dois'],
                'crossref_checks': []
            }
            
            if not ref['dois']:
                no_doi_refs_count += 1
                log_msg = f"  ℹ️ Ref {ref['ref_num']}: No DOI in reference"
                print(log_msg)
                summary_lines.append(log_msg)
                chap_result['references'].append(ref_info)
                continue
                
            for doi in ref['dois']:
                doi_count += 1
                cr_data = query_crossref_doi(doi, cache)
                
                sim_score = 0.0
                if cr_data['status'] == 'OK':
                    valid_doi_count += 1
                    cr_title = cr_data['title']
                    sim_score = title_similarity(cr_title, ref['text'], ref['i_tags'])
                    
                    if sim_score < 0.50:
                        mismatched_count += 1
                        log_msg = (f"  ❌ [MISMATCH!] Ref {ref['ref_num']} DOI {doi}\n"
                                   f"     Cited text: {ref['text'][:120]}...\n"
                                   f"     CrossRef Title: {cr_title}\n"
                                   f"     Similarity Score: {sim_score:.2f}")
                    else:
                        matched_count += 1
                        log_msg = f"  ✅ [MATCH ({sim_score:.2f})] Ref {ref['ref_num']} DOI {doi} -> {cr_title[:70]}"
                else:
                    http_error_count += 1
                    mismatched_count += 1
                    log_msg = f"  ❌ [BAD DOI / {cr_data['status']}] Ref {ref['ref_num']} DOI {doi}: {cr_data.get('error', '')}"
                
                print(log_msg)
                summary_lines.append(log_msg)
                
                ref_info['crossref_checks'].append({
                    'doi': doi,
                    'crossref_data': cr_data,
                    'similarity': sim_score
                })
                
            chap_result['references'].append(ref_info)
        all_results.append(chap_result)
        
    summary_str = (
        f"\n================ EMPIRICAL VERIFICATION SUMMARY ================\n"
        f"Chapters Analyzed: Chapters 01 - 20\n"
        f"Total References: {sum(r['ref_count'] for r in all_results)}\n"
        f"References Without DOI: {no_doi_refs_count}\n"
        f"Total DOIs Checked: {doi_count}\n"
        f"Valid DOIs (200 OK): {valid_doi_count}\n"
        f"HTTP Errors / Dead DOIs: {http_error_count}\n"
        f"Verified Matches (Similarity >= 0.50): {matched_count}\n"
        f"Mismatches / Hallucinated / Dead DOIs: {mismatched_count}\n"
        f"=================================================================\n"
    )
    print(summary_str)
    summary_lines.append(summary_str)
    
    json_path = os.path.join(out_dir, "verification_results.json")
    txt_path = os.path.join(out_dir, "verification_log.txt")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
        
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary_lines))
        
    print(f"Results saved to {json_path} and {txt_path}")

if __name__ == '__main__':
    main()
