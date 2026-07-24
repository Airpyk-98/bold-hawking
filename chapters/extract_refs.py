import os
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import json

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
    
    # find references section
    # it can be under a heading 'References' or 'Structure-Activity Relationships'
    # or just an <ol> at the end.
    
    # Let's find all <ol> tags
    ols = soup.find_all('ol')
    
    # We assume the last <ol> is the references if there are multiple.
    if not ols:
        print(f"No <ol> found in {ch}")
        continue
        
    ref_ol = ols[-1]
    
    for i, li in enumerate(ref_ol.find_all('li', recursive=False)):
        html_str = str(li)
        text_content = li.get_text()
        links = li.find_all('a')
        
        # Check for plain text DOIs or URLs
        # regex for plain text doi not in href
        # actually, just check if the text contains a DOI/URL but there are no links, 
        # or if there is a link but also a plain text DOI.
        
        results.append({
            "chapter": ch,
            "ref_index": i + 1,
            "html": html_str.strip(),
            "text": text_content.strip()
        })

with open('audit_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("Done extracting")
