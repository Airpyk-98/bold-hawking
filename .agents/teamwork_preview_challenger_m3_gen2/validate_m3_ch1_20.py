"""
Validation Harness for Milestone 3 (Chapters 1-20)
Empirical DOI Resolution, CrossRef Title Similarity, and HTML Syntax Audit
"""

import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

CHAPTERS_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

def string_similarity(a, b):
    if not a or not b:
        return 0.0
    a_clean = re.sub(r'[^\w\s]', '', a.lower()).strip()
    b_clean = re.sub(r'[^\w\s]', '', b.lower()).strip()
    return SequenceMatcher(None, a_clean, b_clean).ratio()

def check_doi_http_and_crossref(doi_url):
    # Standardize DOI string
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi_url).strip()
    doi_clean = doi_clean.rstrip('.\'")>]')
    
    if not doi_clean or doi_clean == "https://doi.org/":
        return {
            'doi': doi_url,
            'http_status': 400,
            'resolved_url': None,
            'crossref_title': None,
            'valid': False,
            'error': 'Empty/Malformed DOI URL'
        }
    
    # 1. HTTP Redirect/Resolution Check
    req_head = urllib.request.Request(f"https://doi.org/{doi_clean}", headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
    http_status = None
    resolved_url = None
    try:
        with urllib.request.urlopen(req_head, timeout=10) as resp:
            http_status = resp.status
            resolved_url = resp.geturl()
    except urllib.error.HTTPError as e:
        http_status = e.code
    except Exception as e:
        http_status = str(e)
        
    # 2. CrossRef API Query
    cr_url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    req_cr = urllib.request.Request(cr_url, headers={'User-Agent': 'mailto:verification@example.com'})
    cr_title = None
    try:
        with urllib.request.urlopen(req_cr, timeout=10) as resp_cr:
            if resp_cr.status == 200:
                data = json.loads(resp_cr.read().decode('utf-8'))
                titles = data.get('message', {}).get('title', [])
                if titles:
                    cr_title = titles[0]
    except Exception:
        pass
        
    is_valid = (http_status in [200, 301, 302, 303, 307, 308]) or (cr_title is not None)
    return {
        'doi': doi_clean,
        'doi_url': doi_url,
        'http_status': http_status,
        'resolved_url': resolved_url,
        'crossref_title': cr_title,
        'valid': is_valid
    }

def audit_chapters():
    report = {
        'total_chapters': 20,
        'total_dois': 0,
        'valid_dois': 0,
        'invalid_dois': 0,
        'nested_anchors': 0,
        'syntax_errors': [],
        'details': []
    }
    
    for ch in range(1, 21):
        filename = f"chapter_{ch:02d}.html"
        filepath = os.path.join(CHAPTERS_DIR, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Scan for nested anchor tags
        nested_matches = re.findall(r'<a\b[^>]*>[\s\S]*?<a\b', content, re.IGNORECASE)
        if nested_matches:
            report['nested_anchors'] += len(nested_matches)
            report['syntax_errors'].append({
                'chapter': ch,
                'type': 'nested_anchor',
                'count': len(nested_matches),
                'snippets': nested_matches[:3]
            })
            
        # Parse references and DOIs
        soup = BeautifulSoup(content, 'html.parser')
        ref_items = soup.find_all('li')
        
        for idx, item in enumerate(ref_items, 1):
            ref_text = item.get_text()
            a_tags = item.find_all('a')
            
            for a in a_tags:
                href = a.get('href', '')
                if 'doi.org' in href or '10.' in href:
                    report['total_dois'] += 1
                    res = check_doi_http_and_crossref(href)
                    
                    sim_score = 0.0
                    if res['crossref_title']:
                        sim_score = string_similarity(ref_text, res['crossref_title'])
                        
                    res['cited_text'] = ref_text[:150]
                    res['similarity_score'] = sim_score
                    res['chapter'] = ch
                    res['ref_index'] = idx
                    
                    if res['valid']:
                        report['valid_dois'] += 1
                    else:
                        report['invalid_dois'] += 1
                        
                    report['details'].append(res)
                    
    return report

if __name__ == '__main__':
    results = audit_chapters()
    out_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_challenger_m3_gen2\m3_ch1_20_validation_report.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Validation complete. Report written to {out_path}")
