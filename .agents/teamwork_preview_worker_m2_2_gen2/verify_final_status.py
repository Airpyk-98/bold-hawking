import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout.reconfigure(encoding='utf-8')

class NoRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirection)
headers = {'User-Agent': 'Mozilla/5.0'}

chapters = [f'chapters/chapter_{i:02d}.html' for i in range(8, 15)]

report = []
all_dois_to_test = []

for filepath in chapters:
    print(f"\nVerifying {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Check container
    headings = soup.find_all(lambda tag: tag.name in ['h1','h2','h3','h4','p','span','strong'] and 'references' in tag.get_text().lower())
    ols = soup.find_all('ol')
    p_num = [p for p in soup.find_all('p') if re.match(r'^\s*\d+\.\s+', p.get_text())]
    
    # Check nested <a>
    nested_a = re.findall(r'<a\s+[^>]*>\s*<a\s+[^>]*>.*?</a>\s*</a>', html, re.DOTALL | re.IGNORECASE)
    # Check malformed href
    malformed_href = re.findall(r'href=["\']&lt;a\s+href=.*?', html, re.IGNORECASE)

    # Extract all doi.org links in the file
    dois_in_file = re.findall(r'https?://doi\.org/10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', html)
    dois_clean = [d.rstrip('.,;)"><') for d in set(dois_in_file)]

    ch_summary = {
        "file": filepath,
        "ref_headings_found": len(headings) > 0,
        "ol_count": len(ols),
        "ref_items_count": len(ols[-1].find_all('li')) if ols else 0,
        "remaining_numbered_p": len(p_num),
        "nested_a_count": len(nested_a),
        "malformed_href_count": len(malformed_href),
        "dois_count": len(dois_clean),
        "dois": dois_clean
    }
    report.append(ch_summary)
    
    for d in dois_clean:
        all_dois_to_test.append((filepath, d))

print("\n========================================")
print("STRUCTURE & CLEANUP VERIFICATION SUMMARY:")
for r in report:
    print(f"{r['file']}: OL_Count={r['ol_count']} | Ref_LIs={r['ref_items_count']} | Leftover_<p>={r['remaining_numbered_p']} | Nested_<a>={r['nested_a_count']} | Bad_href={r['malformed_href_count']} | DOIs={r['dois_count']}")

print(f"\n========================================")
print(f"TESTING ALL {len(set([d for f,d in all_dois_to_test]))} UNIQUE DOI LINKS ACROSS CHAPTERS 8-14...")

doi_test_results = {}
for filepath, doi_url in all_dois_to_test:
    if doi_url in doi_test_results:
        continue
    req = urllib.request.Request(doi_url, headers=headers)
    try:
        resp = opener.open(req, timeout=5)
        code = resp.getcode()
        doi_test_results[doi_url] = (code in [200, 301, 302, 303, 307, 308], code)
    except urllib.error.HTTPError as e:
        doi_test_results[doi_url] = (e.code in [200, 301, 302, 303, 307, 308], e.code)
    except Exception as e:
        doi_test_results[doi_url] = (False, str(e))

print("DOI LINK TEST RESULTS:")
all_pass = True
for d, (ok, code) in doi_test_results.items():
    status_str = "PASS (200 OK / 302 Redirect)" if ok else f"FAIL ({code})"
    if not ok:
        all_pass = False
    print(f"  {d:55s} -> {status_str}")

print("\n========================================")
if all_pass:
    print("ALL DOI LINKS RETURNED 200 OK / 302 RESOLVED STATUS! VERIFICATION SUCCESSFUL!")
else:
    print("SOME DOI LINKS FAILED VERIFICATION!")

with open('.agents/teamwork_preview_worker_m2_2_gen2/final_verification_output.json', 'w', encoding='utf-8') as f:
    json.dump({"structure_report": report, "doi_tests": doi_test_results, "all_pass": all_pass}, f, indent=2)
