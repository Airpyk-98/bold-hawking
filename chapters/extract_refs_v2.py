import os
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import json
import time

chapters = [
    "chapter_42.html",
    "chapter_43.html",
    "chapter_44.html",
    "chapter_45.html",
    "chapter_46.html",
    "chapter_47.html",
    "chapter_48.html",
    "chapter_49.html",
    "chapter_50.html",
]

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

results = []

for ch in chapters:
    path = os.path.join(base_dir, ch)
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Find heading that contains 'References' or 'Structure-Activity'
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    ref_heading = None
    for h in headings:
        if 'reference' in h.get_text().lower() or 'structure-activity' in h.get_text().lower():
            ref_heading = h
            break
            
    if not ref_heading:
        print(f"No References heading found in {ch}")
        # fallback to last <ol>
        ols = soup.find_all('ol')
        if ols:
            ref_ol = ols[-1]
        else:
            continue
    else:
        # Find the next <ol>
        ref_ol = ref_heading.find_next_sibling('ol')
        if not ref_ol:
            ref_ol = ref_heading.find_next('ol')
            
    if not ref_ol:
        print(f"No <ol> found after heading in {ch}")
        continue
        
    for i, li in enumerate(ref_ol.find_all('li', recursive=False)):
        html_str = str(li)
        text_content = li.get_text()
        links = li.find_all('a')
        hrefs = [a.get('href') for a in links if a.get('href')]
        
        # We need to find plain text links/dois
        # regex for plain text url or doi that is not in a href
        
        results.append({
            "chapter": ch,
            "ref_index": i + 1,
            "html": html_str.strip(),
            "text": text_content.strip(),
            "hrefs": hrefs
        })

with open('audit_results_v2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("Done extracting v2")
