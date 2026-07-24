import re
from bs4 import BeautifulSoup
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

chapters = [f"chapter_{i}.html" for i in range(60, 69)]
errors = []

for ch in chapters:
    try:
        with open(ch, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
    except Exception as e:
        print(f"Could not read {ch}: {e}")
        continue
    
    # Find heading that contains 'Reference' or 'Structure-Activity Relationships'
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'span'])
    ref_heading = None
    for h in reversed(headings):
        text = h.get_text().lower()
        if 'reference' in text or 'structure-activity relationship' in text:
            ref_heading = h
            break
    
    # Also check if it's just the last ol
    ols = soup.find_all('ol')
    refs_elements = []
    
    if ols:
        # Check the last ol
        refs_elements = ols[-1].find_all('li')
    else:
        # Maybe p tags like in chapter 67?
        if ref_heading:
            # find all siblings after ref_heading
            curr = ref_heading.find_parent('p') if ref_heading.name in ['strong', 'span'] else ref_heading
            if curr:
                for sibling in curr.find_next_siblings():
                    if sibling.name == 'p' or sibling.name == 'li':
                        refs_elements.append(sibling)

    if not refs_elements:
        print(f"Could not find references in {ch}")
        continue
        
    for i, el in enumerate(refs_elements):
        raw_text = el.get_text()
        a_tags = el.find_all('a')
        
        # 1. Check for DOIs in raw text not in a tag
        doi_match = re.search(r'(10\.\d{4,9}/[-._;()/:A-Z0-9]+)', raw_text, re.I)
        if doi_match:
            doi = doi_match.group(1)
            in_a_tag = False
            for a in a_tags:
                if a.has_attr('href') and doi in a['href']:
                    in_a_tag = True
                    if not a['href'].startswith('https://doi.org/'):
                        errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {raw_text.strip()}\n- **Error:** DOI in link but not starting with https://doi.org/ (Found: {a['href']})\n- **Proposed Correction:** Replace DOI link with `https://doi.org/{doi}`")
                    break
            
            if not in_a_tag:
                errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {raw_text.strip()}\n- **Error:** Unclickable plain text link / DOI\n- **Proposed Correction:** Wrap in `<a href=\"https://doi.org/{doi}\">https://doi.org/{doi}</a>`")
        
        # 2. Check for plain text URLs not in a tag (http or https)
        # We need to find URLs in text. Let's do a simple regex
        urls_in_text = re.findall(r'(https?://[^\s]+)', raw_text)
        for url in urls_in_text:
            url = url.rstrip(').,;')
            in_a_tag = False
            for a in a_tags:
                if a.has_attr('href') and url in a['href']:
                    in_a_tag = True
                    break
            if not in_a_tag:
                errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {raw_text.strip()}\n- **Error:** Unclickable plain text link / URL\n- **Proposed Correction:** Wrap in `<a href=\"{url}\">{url}</a>`")
        
        # 3. Check for JSTOR links in text
        if 'jstor.org' in raw_text.lower():
            errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {raw_text.strip()}\n- **Error:** JSTOR link found\n- **Proposed Correction:** Convert JSTOR handle to proper CrossRef DOI")

        # 4. Validate DOIs by making a request
        for a in a_tags:
            href = a.get('href', '')
            if 'doi.org' in href:
                try:
                    resp = requests.get(href, allow_redirects=True, timeout=5, verify=False)
                    if resp.status_code in [404]:
                        errors.append(f"**Chapter {ch[-7:-5]}**:\n- **Reference Text:** {raw_text.strip()}\n- **Error:** Broken DOI (404 Not Found) for {href}\n- **Proposed Correction:** Use CrossRef API to find correct DOI")
                except requests.exceptions.RequestException as e:
                    pass

for e in errors:
    print(e)
    print()
print("Done v2.")
