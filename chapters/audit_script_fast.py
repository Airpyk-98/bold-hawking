import os
import re
import urllib.request
import urllib.error
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

chapters = [
    f"chapter_{i}.html" for i in range(42, 51)
]
base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

reports = []
urls_to_check = set()

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        urllib.request.urlopen(req, timeout=10)
        return url, "OK"
    except urllib.error.HTTPError as e:
        if e.code in [403, 405, 401]:
            return url, "BOT_BLOCK"
        return url, f"HTTP_ERROR_{e.code}"
    except Exception as e:
        return url, f"ERROR_{str(e)}"

# First phase: parse
items_by_chapter = []

for ch in chapters:
    path = os.path.join(base_dir, ch)
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    ref_heading = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong', 'span'] and tag.get_text() and 'References' in tag.get_text().strip())
    
    if not ref_heading:
        reports.append(f"Chapter {ch}: No References heading found.")
        continue
        
    parent = ref_heading.parent
    if ref_heading.name in ['strong', 'span']:
        ref_heading = ref_heading.find_parent('p') or ref_heading
        
    siblings = ref_heading.find_next_siblings()
    
    ol_tag = None
    p_refs = []
    
    for sib in siblings:
        if sib.name == 'ol':
            ol_tag = sib
            break
        elif sib.name == 'p' and sib.get_text().strip() and re.match(r'^\d+\.', sib.get_text().strip()):
            p_refs.append(sib)
            
    if not ol_tag and p_refs:
        reports.append(f"Chapter {ch}: References are in <p> tags instead of <ol>. Found {len(p_refs)} references.")
        items_to_check = p_refs
    elif ol_tag:
        items_to_check = ol_tag.find_all('li', recursive=False)
    else:
        reports.append(f"Chapter {ch}: No references found after heading.")
        continue
        
    for item in items_to_check:
        html_str = str(item)
        text = item.get_text().strip()
        links = item.find_all('a')
        hrefs = [a.get('href') for a in links if a.get('href')]
        
        doi_match = re.search(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', text, re.IGNORECASE)
        if doi_match:
            doi_str = doi_match.group(0).rstrip('.')
            in_href = any(doi_str in h for h in hrefs)
            if not in_href:
                reports.append(f"Chapter {ch}: Plain text DOI found: {doi_str} (in text: '{text[:50]}...')")
                
        for a in links:
            href = a.get('href')
            if not href: continue
            
            if 'doi.org' in href:
                if not href.startswith('https://doi.org/'):
                    reports.append(f"Chapter {ch}: Malformed DOI link (must start with https://doi.org/): {href}")
                urls_to_check.add(href)
            elif '10.' in href and 'doi' not in href:
                reports.append(f"Chapter {ch}: Link might be a plain DOI without https://doi.org/: {href}")
            else:
                urls_to_check.add(href)
                
        # Register the chapter and links to associate back if broken
        items_by_chapter.append((ch, hrefs))

# Second phase: check URLs concurrently
url_status = {}
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(check_url, url): url for url in urls_to_check}
    for future in as_completed(futures):
        url, status = future.result()
        url_status[url] = status

for ch, hrefs in items_by_chapter:
    for href in hrefs:
        if href in url_status:
            status = url_status[href]
            if status not in ["OK", "BOT_BLOCK"]:
                reports.append(f"Chapter {ch}: Broken link ({status}): {href}")

with open('audit_report_fast.txt', 'w', encoding='utf-8') as f:
    for r in reports:
        f.write(r + '\n')

print("Fast audit script finished.")
