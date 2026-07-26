import os
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapter_files = [f"chapter_{str(i).zfill(2)}.html" for i in range(1, 8)]

results = []

def check_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.getcode(), str(resp.geturl())
    except urllib.error.HTTPError as e:
        return e.code, str(e.url)
    except Exception as e:
        return f"Error: {str(e)}", url

def query_crossref(title):
    headers = {'User-Agent': 'mailto:explorer@antigravity.org'}
    clean_title = re.sub(r'[^\w\s]', '', title)[:120]
    encoded = urllib.parse.quote(clean_title)
    url = f"https://api.crossref.org/works?query.bibliographic={encoded}&rows=3"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get("message", {}).get("items", [])
            matches = []
            for item in items:
                matches.append({
                    "DOI": item.get("DOI"),
                    "title": item.get("title", [""])[0] if item.get("title") else "",
                    "score": item.get("score")
                })
            return matches
    except Exception as e:
        return f"Crossref lookup failed: {e}"

for ch_file in chapter_files:
    path = os.path.join(base_dir, ch_file)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Locate reference section
    ref_headers = soup.find_all(re.compile('^h[1-6]$'), string=re.compile(r'References', re.IGNORECASE))
    if not ref_headers:
        # Check elements containing References
        ref_headers = [el for el in soup.find_all(['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if 'references' in el.get_text().lower()]
    
    ols = soup.find_all('ol')
    
    ref_ol = None
    if ref_headers:
        # find ol after header
        for header in ref_headers:
            next_ol = header.find_next('ol')
            if next_ol:
                ref_ol = next_ol
                break
    
    if not ref_ol and ols:
        ref_ol = ols[-1]
    
    chapter_data = {
        "file": ch_file,
        "has_ref_header": len(ref_headers) > 0,
        "has_ol": ref_ol is not None,
        "references": []
    }
    
    if ref_ol:
        lis = ref_ol.find_all('li', recursive=False)
        if not lis:
            lis = ref_ol.find_all('li')
            
        for idx, li in enumerate(lis, 1):
            raw_html = str(li)
            text = li.get_text(separator=" ", strip=True)
            
            # find all <a> tags inside li
            anchors = []
            for a in li.find_all('a'):
                anchors.append({
                    "href": a.get('href'),
                    "text": a.get_text(strip=True),
                    "raw_a": str(a)
                })
            
            # extract potential DOIs using regex from text and raw_html
            doi_matches = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text + " " + raw_html)
            doi_matches = list(set(doi_matches))
            # clean trailing dots/brackets from DOIs
            doi_matches = [re.sub(r'[\.,;\)]+$', '', d) for d in doi_matches]
            
            # Extract URLs
            url_matches = re.findall(r'https?://[^\s<">]+', text + " " + raw_html)
            url_matches = [u.rstrip('.,;)') for u in url_matches]
            url_matches = list(set(url_matches))
            
            ref_item = {
                "ref_num": idx,
                "text": text,
                "raw_html": raw_html,
                "anchors": anchors,
                "doi_matches": doi_matches,
                "url_matches": url_matches
            }
            chapter_data["references"].append(ref_item)
    
    results.append(chapter_data)

out_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_1\extracted_raw_m1.json"
with open(out_path, 'w', encoding='utf-8') as out_f:
    json.dump(results, out_f, indent=2)

print(f"Extracted data for {len(results)} chapters.")
