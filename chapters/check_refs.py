import re
from bs4 import BeautifulSoup
import os
import requests

chapters = [f"chapter_{i}.html" for i in range(60, 69)]

errors = []

for ch in chapters:
    try:
        with open(ch, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
    except Exception as e:
        print(f"Could not read {ch}: {e}")
        continue
    
    # find all ol tags
    ols = soup.find_all('ol')
    if not ols:
        print(f"{ch} has no <ol> tag")
        continue
    
    # usually the last ol is the references
    ref_ol = ols[-1]
    
    lis = ref_ol.find_all('li')
    for i, li in enumerate(lis):
        text = li.get_text()
        html = str(li)
        
        # Check for plain text doi or URLs
        # any url or doi pattern not inside an href
        
        # We can extract all <a> tags
        a_tags = li.find_all('a')
        
        # Find raw text that looks like a DOI or http
        raw_text = li.get_text()
        
        # check if it has a doi string like 10.xxxx/xxxx
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', raw_text, re.I)
        
        if doi_match:
            doi = doi_match.group(0)
            # check if this doi is in an href
            in_a_tag = False
            for a in a_tags:
                if a.has_attr('href') and doi in a['href']:
                    in_a_tag = True
                    # Check if it starts with https://doi.org/
                    if not a['href'].startswith('https://doi.org/'):
                        errors.append(f"{ch} Ref {i+1}: DOI in link but not starting with https://doi.org/ (Found: {a['href']})")
                    break
            
            if not in_a_tag:
                errors.append(f"{ch} Ref {i+1}: Plain text DOI found: {doi}. Proposed Correction: Wrap in <a href=\"https://doi.org/{doi}\">https://doi.org/{doi}</a>")
        else:
            # Maybe JSTOR?
            if 'jstor.org' in raw_text.lower():
                errors.append(f"{ch} Ref {i+1}: JSTOR link found. Should check if CrossRef DOI exists.")
                
        # Check all a_tags
        for a in a_tags:
            href = a.get('href', '')
            if href.startswith('http'):
                # We should check if it resolves, but let's do this in a second pass
                pass
            else:
                errors.append(f"{ch} Ref {i+1}: Link does not start with http: {href}")
                
for e in errors:
    print(e)
print("Done static analysis.")
