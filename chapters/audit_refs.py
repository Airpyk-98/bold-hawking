import os
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import json

directory = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapters = [f"chapter_{str(i).zfill(2)}.html" for i in range(15, 24)]

def check_doi(doi):
    url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        urllib.request.urlopen(req)
        return "OK"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:
        return str(e)

for chapter in chapters:
    filepath = os.path.join(directory, chapter)
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    print(f"\n--- {chapter} ---")
    
    # Find headers containing "References" or "Structure-Activity Relationships"
    headers = soup.find_all(re.compile('^h[1-6]$'), string=re.compile('References|Structure-Activity Relationships', re.IGNORECASE))
    
    if not headers:
        # Check last <ol> in the document
        ols = soup.find_all('ol')
        if ols:
            refs = ols[-1]
            print("Found <ol> at end, no header.")
        else:
            print("No references found.")
            continue
    else:
        # Find the <ol> following the header
        header = headers[-1]
        refs = header.find_next_sibling('ol')
        if not refs:
            print("No <ol> found after header.")
            continue
            
    for i, li in enumerate(refs.find_all('li'), 1):
        text = li.get_text()
        links = li.find_all('a')
        link_hrefs = [a['href'] for a in links]
        
        print(f"Ref {i}: {text.strip()[:100]}...")
        if not links:
            print("  [ERROR] No <a> tags found.")
            # check if there's a plain text DOI or URL
            if "doi.org" in text or "10." in text or "http" in text:
                print("    -> Plain text link detected.")
        else:
            for href in link_hrefs:
                if "doi.org" in href or href.startswith("10."):
                    status = check_doi(href)
                    print(f"  [LINK] {href} -> {status}")
                else:
                    print(f"  [LINK] {href} -> (Not checked)")
