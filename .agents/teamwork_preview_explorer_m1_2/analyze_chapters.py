import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

chapters_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapter_files = [f"chapter_{str(i).zfill(2)}.html" for i in range(8, 15)]

def check_doi_crossref(doi):
    url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), resp.geturl()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e), None

def search_crossref_bibliographic(ref_text):
    clean_text = re.sub(r'https?://[^\s]+', '', ref_text)
    clean_text = re.sub(r'doi:[^\s]+', '', clean_text, flags=re.IGNORECASE)
    query = urllib.parse.quote(clean_text[:200])
    url = f"https://api.crossref.org/works?query.bibliographic={query}&rows=3"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:explorer@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                title = item.get('title', [''])[0]
                doi = item.get('DOI', '')
                results.append({'title': title, 'doi': doi})
            return results
    except Exception as e:
        return []

all_chapters_data = {}

for ch_file in chapter_files:
    file_path = os.path.join(chapters_dir, ch_file)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    refs_header = soup.find(re.compile(r'^h[1-6]$'), string=re.compile(r'References', re.IGNORECASE))
    ol_tag = None
    if refs_header:
        # look for next ol
        ol_tag = refs_header.find_next("ol")
    if not ol_tag:
        ols = soup.find_all("ol")
        if ols:
            ol_tag = ols[-1]
            
    ch_data = {
        "file": ch_file,
        "has_refs_header": refs_header is not None,
        "refs_header_tag": refs_header.name if refs_header else None,
        "refs_header_text": refs_header.get_text() if refs_header else None,
        "total_references": 0,
        "references": []
    }
    
    if ol_tag:
        li_items = ol_tag.find_all("li", recursive=False)
        if not li_items:
            li_items = ol_tag.find_all("li")
        ch_data["total_references"] = len(li_items)
        
        for idx, li in enumerate(li_items, 1):
            raw_html = str(li)
            text = li.get_text(strip=True)
            a_tags = li.find_all("a")
            links = []
            for a in a_tags:
                links.append({
                    "href": a.get("href", ""),
                    "text": a.get_text(strip=True),
                    "raw_a_tag": str(a)
                })
            
            # Check for plain text DOIs or URLs
            doi_match = re.findall(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', text, re.IGNORECASE)
            url_match = re.findall(r'https?://[^\s>"]+', text)
            
            ref_info = {
                "index": idx,
                "text": text,
                "raw_html": raw_html,
                "anchor_tags": links,
                "plain_dois_in_text": doi_match,
                "urls_in_text": url_match
            }
            ch_data["references"].append(ref_info)
            
    all_chapters_data[ch_file] = ch_data

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\extracted_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_chapters_data, f, indent=2)

print("Finished parsing raw HTML for chapters 8-14.")
