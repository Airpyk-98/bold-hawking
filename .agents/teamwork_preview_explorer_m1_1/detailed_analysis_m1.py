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

chapters_report = []

def check_http_status(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.getcode(), str(resp.geturl()), None
    except urllib.error.HTTPError as e:
        return e.code, str(e.url), f"HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return 0, url, str(e)

def query_crossref(query_str):
    headers = {'User-Agent': 'mailto:explorer1@antigravity.org'}
    clean = re.sub(r'[^\w\s]', ' ', query_str)[:150]
    encoded = urllib.parse.quote(clean.strip())
    url = f"https://api.crossref.org/works?query.bibliographic={encoded}&rows=2"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get("message", {}).get("items", [])
            results = []
            for item in items:
                title = item.get("title", [""])[0] if item.get("title") else ""
                doi = item.get("DOI", "")
                score = item.get("score", 0)
                container = item.get("container-title", [""])[0] if item.get("container-title") else ""
                year = ""
                if "published-print" in item and "date-parts" in item["published-print"]:
                    year = str(item["published-print"]["date-parts"][0][0])
                elif "published-online" in item and "date-parts" in item["published-online"]:
                    year = str(item["published-online"]["date-parts"][0][0])
                results.append({
                    "doi": doi,
                    "title": title,
                    "container": container,
                    "year": year,
                    "score": score
                })
            return results
    except Exception as e:
        return f"Error: {e}"

for ch_file in chapter_files:
    path = os.path.join(base_dir, ch_file)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check headers
    h_refs = [h for h in soup.find_all(['h1','h2','h3','h4','h5','h6','p','div']) if 'reference' in h.get_text().lower()]
    
    # Locate all <ol> tags
    ols = soup.find_all('ol')
    
    ref_ol = None
    if ols:
        # Check if any ol is specifically after a references header or at the end
        ref_ol = ols[-1] # default to last ol
    
    ch_info = {
        "chapter_filename": ch_file,
        "chapter_number": int(ch_file.replace("chapter_", "").replace(".html", "")),
        "total_ols_in_doc": len(ols),
        "has_references_section": len(h_refs) > 0,
        "reference_headers": [h.get_text().strip() for h in h_refs],
        "references": []
    }
    
    if ref_ol:
        lis = ref_ol.find_all('li', recursive=False)
        if not lis:
            lis = ref_ol.find_all('li')
        
        for idx, li in enumerate(lis, 1):
            raw_html = str(li).strip()
            text = li.get_text(separator=" ", strip=True)
            
            # HTML structure issues detection
            nested_a_count = raw_html.count('<a href')
            has_nested_a = False
            if '<a ' in raw_html:
                a_soup = BeautifulSoup(raw_html, 'html.parser')
                outer_a = a_soup.find_all('a')
                for a_tag in outer_a:
                    if a_tag.find('a'):
                        has_nested_a = True
                        break
            
            # extract all anchor tags
            anchors_detail = []
            for a in li.find_all('a'):
                anchors_detail.append({
                    "href": a.get('href', ''),
                    "text": a.get_text(strip=True),
                    "outer_html": str(a)
                })
            
            # Check for plain text DOI/URL not inside href
            hrefs_combined = " ".join([a['href'] for a in anchors_detail])
            
            # Regex for DOIs
            doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+'
            found_dois = list(set([re.sub(r'[\.,;\)]+$', '', d) for d in re.findall(doi_pattern, text + " " + raw_html)]))
            
            # Regex for URLs
            url_pattern = r'https?://[^\s<">]+'
            found_urls = list(set([u.rstrip('.,;)') for u in re.findall(url_pattern, text + " " + raw_html)]))
            
            # Check if DOI in text is missing anchor tag or has plain text doi
            has_plain_text_doi = False
            for d in found_dois:
                if d not in hrefs_combined and f"10.{d.split('10.',1)[-1]}" not in hrefs_combined:
                    has_plain_text_doi = True
            
            # Check DOI HTTP status for all found DOIs
            doi_audit = []
            for d in found_dois:
                doi_url = d if d.startswith('http') else f"https://doi.org/{d}"
                status_code, final_url, err = check_http_status(doi_url)
                
                # Crossref check if 404 or bad status or to verify title match
                crossref_info = None
                if status_code != 200 or True: # We check crossref for title matching as well
                    # extract title from text: standard APA "(Year). Title. Journal..."
                    title_match = re.search(r'\(\d{4}[a-z]?\)\.\s*([^\.]+)\.', text)
                    title_query = title_match.group(1) if title_match else text[:100]
                    crossref_info = query_crossref(title_query)
                
                doi_audit.append({
                    "extracted_doi": d,
                    "doi_url": doi_url,
                    "http_status": status_code,
                    "final_url": final_url,
                    "http_error": err,
                    "crossref_match": crossref_info
                })
            
            # If no DOIs found, run Crossref search using reference title to see if a DOI exists!
            if not found_dois and len(text) > 20:
                title_match = re.search(r'\(\d{4}[a-z]?\)\.\s*([^\.]+)\.', text)
                title_query = title_match.group(1) if title_match else text[:100]
                possible_crossref = query_crossref(title_query)
            else:
                possible_crossref = None

            # Detect formatting anomalies (missing italics tag, bad unicode, odd chars)
            has_missing_italics = '<i>' not in raw_html and '<em>' not in raw_html
            has_unreplaced_placeholders = '' in text or '\ufffd' in text
            
            ref_entry = {
                "ref_num": idx,
                "text": text,
                "raw_html": raw_html,
                "anchors": anchors_detail,
                "found_dois": found_dois,
                "found_urls": found_urls,
                "has_nested_a_tags": has_nested_a,
                "has_plain_text_doi": has_plain_text_doi,
                "has_unreplaced_placeholders": has_unreplaced_placeholders,
                "doi_audit": doi_audit,
                "possible_missing_doi_crossref": possible_crossref
            }
            
            ch_info["references"].append(ref_entry)
            
    chapters_report.append(ch_info)

out_file = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_1\m1_detailed_audit.json"
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(chapters_report, f, indent=2, ensure_ascii=False)

print(f"Audit completed for {len(chapters_report)} chapters. Report written to {out_file}.")
