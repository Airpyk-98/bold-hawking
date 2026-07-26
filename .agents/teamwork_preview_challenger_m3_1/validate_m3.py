import os
import re
import html
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

CHAPTERS_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
TARGET_CHAPTERS = [f"chapter_{i:02d}.html" for i in range(1, 21)]

class SyntaxChecker(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tag_stack = []
        self.nested_anchors = []
        self.syntax_errors = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if 'a' in self.tag_stack:
                self.nested_anchors.append({
                    'file': self.filename,
                    'line': self.getpos()[0],
                    'col': self.getpos()[1],
                    'context': f"Nested <a> inside parent <a> stack: {self.tag_stack}"
                })
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.tag_stack:
            while self.tag_stack:
                popped = self.tag_stack.pop()
                if popped == tag:
                    break
        else:
            self.syntax_errors.append({
                'file': self.filename,
                'line': self.getpos()[0],
                'col': self.getpos()[1],
                'error': f"Unmatched closing tag </{tag}>"
            })

def extract_doi_links_refined(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    found_entries = []

    # 1. Extract from href="..."
    href_matches = re.findall(r'href=["\']([^"\']*doi\.org[^"\']*)["\']', content, re.IGNORECASE)
    for raw_href in href_matches:
        # Unescape HTML entities e.g. &lt; -> <, &gt; -> >
        unescaped = html.unescape(raw_href)
        found_entries.append({
            'raw': raw_href,
            'clean': unescaped,
            'source': 'href'
        })

    # 2. Extract plain text DOIs (not inside href)
    # Remove hrefs from content to avoid duplicate matching
    content_no_href = re.sub(r'href=["\'][^"\']*["\']', '', content)
    raw_matches = re.findall(r'https?://(?:dx\.)?doi\.org/[^\s<>"\'\]]+', content_no_href, re.IGNORECASE)
    for raw_url in raw_matches:
        clean_url = raw_url.rstrip('.,;)')
        found_entries.append({
            'raw': raw_url,
            'clean': clean_url,
            'source': 'text'
        })

    return found_entries

def check_html_syntax(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(file_path)
    
    # 1. Regex check for nested anchors: <a ...> ... <a ...> ... </a> ... </a>
    nested_regex = r'<a\b[^>]*>(?:(?!</a>).)*?<a\b[^>]*>'
    regex_matches = re.findall(nested_regex, content, re.IGNORECASE | re.DOTALL)
    
    # 2. HTMLParser stack check
    parser = SyntaxChecker(filename)
    try:
        parser.feed(content)
    except Exception as e:
        parser.syntax_errors.append({'file': filename, 'error': str(e)})

    return regex_matches, parser.nested_anchors, parser.syntax_errors

def check_doi_http(doi_url, timeout=12):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    
    # Ensure scheme
    if not doi_url.startswith('http://') and not doi_url.startswith('https://'):
        target_url = 'https://' + doi_url
    else:
        target_url = doi_url

    # Handle special characters like < > inside DOI by percent encoding if needed
    parsed = urllib.parse.urlparse(target_url)
    encoded_path = urllib.parse.quote(parsed.path, safe='/()[]:;-&+=.,%')
    encoded_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, encoded_path, parsed.params, parsed.query, parsed.fragment))

    req = urllib.request.Request(encoded_url, headers=headers)
    
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
        with opener.open(req, timeout=timeout) as resp:
            status = resp.status
            final_url = resp.geturl()
            # 200 OK, 202 Accepted, 301, 302, 303, 307, 308 are all success
            is_success = status in [200, 201, 202, 203, 204, 301, 302, 303, 307, 308]
            return {
                'url': doi_url,
                'tested_url': encoded_url,
                'status': status,
                'final_url': final_url,
                'success': is_success,
                'error': None
            }
    except urllib.error.HTTPError as e:
        final_url = getattr(e, 'filename', getattr(e, 'url', target_url))
        is_redirected_away_from_doi = 'doi.org' not in urllib.parse.urlparse(final_url).netloc
        
        # 2xx success statuses or publisher Cloudflare bot-blocks (403/401/429) after resolving from doi.org
        is_success = e.code in [200, 201, 202, 203, 204, 301, 302, 303, 307, 308] or (is_redirected_away_from_doi and e.code in [403, 401, 429])
        
        return {
            'url': doi_url,
            'tested_url': encoded_url,
            'status': e.code,
            'final_url': final_url,
            'success': is_success,
            'is_publisher_block': e.code in [403, 401, 429] and is_redirected_away_from_doi,
            'error': f"HTTP Error {e.code}"
        }
    except Exception as e:
        return {
            'url': doi_url,
            'tested_url': encoded_url,
            'status': 0,
            'final_url': None,
            'success': False,
            'error': str(e)
        }

def main():
    print("=== STARTING MILESTONE 3 REFINED EMPIRICAL VALIDATION ===")
    all_chapter_details = {}
    unique_dois_map = {} # clean_url -> list of chapters

    nested_anchor_findings = []
    syntax_error_findings = []

    for chapter_file in TARGET_CHAPTERS:
        file_path = os.path.join(CHAPTERS_DIR, chapter_file)
        if not os.path.exists(file_path):
            continue

        # HTML Syntax
        regex_nested, parser_nested, syntax_errs = check_html_syntax(file_path)
        if regex_nested or parser_nested:
            nested_anchor_findings.append({
                'chapter': chapter_file,
                'regex_count': len(regex_nested),
                'parser_details': parser_nested
            })
        if syntax_errs:
            syntax_error_findings.append({
                'chapter': chapter_file,
                'errors': syntax_errs
            })

        # DOI Extraction
        entries = extract_doi_links_refined(file_path)
        chapter_dois = []
        for item in entries:
            clean_url = item['clean']
            chapter_dois.append(clean_url)
            if clean_url not in unique_dois_map:
                unique_dois_map[clean_url] = []
            unique_dois_map[clean_url].append({'chapter': chapter_file, 'raw': item['raw'], 'source': item['source']})

        all_chapter_details[chapter_file] = {
            'count': len(chapter_dois),
            'entries': entries
        }

    print(f"Chapters Scanned: {len(TARGET_CHAPTERS)}")
    print(f"Total Unique DOI URLs: {len(unique_dois_map)}")
    print(f"Nested Anchor Findings: {len(nested_anchor_findings)}")
    print(f"Syntax Error Findings: {len(syntax_error_findings)}")

    # Concurrent HTTP verification
    print("\n--- Verifying DOI HTTP Statuses ---")
    doi_http_results = {}
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_doi = {executor.submit(check_doi_http, doi): doi for doi in unique_dois_map.keys()}
        for future in as_completed(future_to_doi):
            doi = future_to_doi[future]
            res = future.result()
            doi_http_results[doi] = res
            status_str = f"HTTP {res['status']}" if res['status'] != 0 else "ERROR"
            outcome = "PASS" if res['success'] else "FAIL"
            print(f"[{outcome}] {doi} -> {status_str} (Final: {res['final_url']})")

    passed_list = [r for r in doi_http_results.values() if r['success']]
    failed_list = [r for r in doi_http_results.values() if not r['success']]

    pass_rate = round(len(passed_list) / len(unique_dois_map) * 100, 2) if unique_dois_map else 100.0

    summary = {
        'total_chapters': len(TARGET_CHAPTERS),
        'nested_anchor_violations': len(nested_anchor_findings),
        'html_syntax_errors': len(syntax_error_findings),
        'unique_doi_count': len(unique_dois_map),
        'passed_doi_count': len(passed_list),
        'failed_doi_count': len(failed_list),
        'pass_rate_percent': pass_rate,
        'failures': [{
            'url': f['url'],
            'status': f['status'],
            'final_url': f['final_url'],
            'error': f['error'],
            'occurrences': unique_dois_map[f['url']]
        } for f in failed_list]
    }

    report_path = os.path.join(os.path.dirname(__file__), 'validation_summary.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("\n=== FINAL EMPIRICAL SUMMARY ===")
    print(f"Nested Anchor Violations: {summary['nested_anchor_violations']}")
    print(f"HTML Syntax Errors: {summary['html_syntax_errors']}")
    print(f"DOI Pass Rate: {summary['pass_rate_percent']}% ({summary['passed_doi_count']}/{summary['unique_doi_count']})")
    if failed_list:
        print("\nFailed DOIs Detail:")
        for fail in summary['failures']:
            print(f" - {fail['url']}")
            print(f"   Status: {fail['status']}, Error: {fail['error']}, Final URL: {fail['final_url']}")
            print(f"   Occurrences: {fail['occurrences']}")

if __name__ == '__main__':
    main()
