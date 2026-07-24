import re
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

chapters = [f"chapter_{i}.html" for i in range(60, 69)]
errors = []

for ch in chapters:
    try:
        with open(ch, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Could not read {ch}: {e}")
        continue
        
    # Check for JSTOR
    if 'jstor.org' in content.lower():
        errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Error:** JSTOR link found\n- **Proposed Correction:** Convert JSTOR handle to proper CrossRef DOI")
        
    # Check for DOIs. We use a regex for DOIs:
    # 10.\d{4,9}/[-._;()/:A-Z0-9]+
    # Since we are matching raw HTML, we can find all occurrences of DOIs.
    # We want to make sure EVERY DOI is part of `href="https://doi.org/10.xxxx"`
    # or `>https://doi.org/10.xxxx<`
    
    # Let's find all DOIs
    dois = re.findall(r'(10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+)', content)
    # Dedup
    dois = list(set(dois))
    
    for doi in dois:
        # Strip trailing punctuation just in case
        clean_doi = doi.rstrip('.,;)')
        
        # We need to verify if `clean_doi` is properly wrapped in an anchor tag pointing to https://doi.org/{clean_doi}
        # Check if the exact string `href="https://doi.org/{clean_doi}"` exists
        expected_href = f'href="https://doi.org/{clean_doi}"'
        
        if expected_href not in content:
            # Maybe it uses http?
            if f'href="http://doi.org/{clean_doi}"' in content:
                errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {clean_doi}\n- **Error:** DOI uses http instead of https\n- **Proposed Correction:** Update to https://doi.org/{clean_doi}")
            else:
                errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {clean_doi}\n- **Error:** Unclickable plain text link / DOI\n- **Proposed Correction:** Wrap in `<a href=\"https://doi.org/{clean_doi}\">https://doi.org/{clean_doi}</a>`")
                
        # Validate the DOI online
        url = f"https://doi.org/{clean_doi}"
        try:
            resp = requests.get(url, allow_redirects=True, timeout=5, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 404:
                errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {clean_doi}\n- **Error:** Broken DOI (404 Not Found) for {url}\n- **Proposed Correction:** Use CrossRef API to find correct DOI")
        except requests.exceptions.RequestException:
            pass

    # Check for any plain URLs not in hrefs (heuristic)
    # We'll just look for http:// or https:// and see if they are inside an href or src
    
for e in set(errors):
    print(e)
    print()
print("Done v3.")
