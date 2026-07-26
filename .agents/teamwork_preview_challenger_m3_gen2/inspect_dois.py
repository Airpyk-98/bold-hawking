import os
import re
from bs4 import BeautifulSoup

chapters_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

total_dois = 0
ch_dois = {}

for ch in range(1, 21):
    filename = f"chapter_{ch:02d}.html"
    filepath = os.path.join(chapters_dir, filename)
    if not os.path.exists(filepath):
        print(f"File missing: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    a_tags = soup.find_all('a')
    
    doi_links = []
    for a in a_tags:
        href = a.get('href', '')
        text = a.get_text()
        if 'doi.org' in href or 'doi.org' in text or '10.' in href:
            doi_links.append((href, text, a.parent.get_text()[:100] if a.parent else ""))
            
    raw_dois = re.findall(r'https?://doi\.org/[^\s"\'<>]+', content)
    
    print(f"Chapter {ch:02d}: {len(a_tags)} <a> tags, {len(doi_links)} DOI <a> tags, {len(raw_dois)} regex DOIs")
    ch_dois[ch] = {
        'a_tags': len(a_tags),
        'doi_links': doi_links,
        'raw_dois': raw_dois
    }
    total_dois += len(doi_links)

print(f"\nTotal DOI links found across Chapters 1-20: {total_dois}")
