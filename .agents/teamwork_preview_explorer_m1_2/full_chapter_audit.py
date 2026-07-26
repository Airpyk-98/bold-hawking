import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import time
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

chapters_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapter_files = [f"chapter_{str(i).zfill(2)}.html" for i in range(8, 15)]

crossref_headers = {'User-Agent': 'mailto:explorer_m1_2@example.com'}
http_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def query_crossref_doi(doi):
    clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi).strip()
    clean_doi = clean_doi.rstrip('.,;)')
    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
    req = urllib.request.Request(url, headers=crossref_headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            msg = data.get('message', {})
            title = msg.get('title', [''])[0]
            authors = []
            for a in msg.get('author', []):
                authors.append(f"{a.get('given', '')} {a.get('family', '')}".strip())
            year = None
            pub = msg.get('published-print') or msg.get('published-online') or msg.get('issued')
            if pub and 'date-parts' in pub and pub['date-parts']:
                year = pub['date-parts'][0][0]
            return {"valid": True, "title": title, "authors": authors, "year": year, "clean_doi": clean_doi}
    except urllib.error.HTTPError as e:
        return {"valid": False, "status": e.code, "clean_doi": clean_doi}
    except Exception as e:
        return {"valid": False, "error": str(e), "clean_doi": clean_doi}

def query_crossref_search(text):
    clean_text = re.sub(r'https?://[^\s]+', '', text)
    clean_text = re.sub(r'doi:[^\s]+', '', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'^\d+\.\s*', '', clean_text)
    clean_text = re.sub(r'\[.*?\]', '', clean_text).strip()
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(clean_text[:250])}&rows=3"
    req = urllib.request.Request(url, headers=crossref_headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                t = item.get('title', [''])[0]
                d = item.get('DOI', '')
                y = None
                pub = item.get('published-print') or item.get('published-online') or item.get('issued')
                if pub and 'date-parts' in pub and pub['date-parts']:
                    y = pub['date-parts'][0][0]
                results.append({'title': t, 'doi': d, 'year': y})
            return results
    except Exception as e:
        return []

all_chapters_audit = {}

for ch_file in chapter_files:
    file_path = os.path.join(chapters_dir, ch_file)
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Locate References heading node
    ref_heading_node = soup.find(string=re.compile(r'^\s*References\s*$', re.IGNORECASE))
    if not ref_heading_node:
        ref_heading_node = soup.find(string=re.compile(r'References', re.IGNORECASE))
        
    heading_container = None
    if ref_heading_node:
        parent = ref_heading_node.parent
        while parent and parent.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']:
            parent = parent.parent
        heading_container = parent
        
    ref_items = []
    container_type = "NONE"
    
    if heading_container:
        # Check if there is an <ol> after heading_container
        next_ol = heading_container.find_next("ol")
        if next_ol:
            container_type = "<ol>"
            for li in next_ol.find_all("li", recursive=False):
                ref_items.append({
                    "raw_html": str(li),
                    "text": li.get_text(strip=True),
                    "element": li
                })
        else:
            # Check if there are following <p> tags with reference numbers e.g. "1.", "2."
            curr = heading_container.find_next_sibling()
            p_items = []
            while curr:
                if curr.name == "p":
                    txt = curr.get_text(strip=True)
                    if re.match(r'^\d+\.\s', txt):
                        p_items.append({
                            "raw_html": str(curr),
                            "text": txt,
                            "element": curr
                        })
                    elif not txt:
                        pass # empty p tag
                    else:
                        # Non numbered text p tag
                        break
                else:
                    break
                curr = curr.find_next_sibling()
            
            if p_items:
                container_type = "<p> list"
                ref_items = p_items
            else:
                container_type = "NO_REF_LIST_FOUND"
    
    ch_result = {
        "chapter_file": ch_file,
        "heading_found": heading_container is not None,
        "heading_tag": heading_container.name if heading_container else None,
        "container_type": container_type,
        "total_references": len(ref_items),
        "references": []
    }
    
    print(f"Auditing {ch_file}: Found {len(ref_items)} references (Container: {container_type})...")
    
    for idx, item in enumerate(ref_items, 1):
        raw_html = item["raw_html"]
        text = item["text"]
        elem = item["element"]
        
        a_tags = elem.find_all("a")
        anchor_info = []
        for a in a_tags:
            anchor_info.append({
                "href": a.get("href", ""),
                "text": a.get_text(strip=True),
                "raw": str(a)
            })
            
        formatting_issues = []
        # Check malformed HTML anchor tags
        if "<a>" in raw_html and "</a>" not in raw_html:
            formatting_issues.append("Unclosed <a> tag")
        if re.search(r'<a[^>]*<a', raw_html):
            formatting_issues.append("Nested <a> tag detected inside <a> tag")
        if re.search(r'href=["\']&lt;a', raw_html) or 'href="<a' in raw_html:
            formatting_issues.append("Malformed href attribute containing embedded <a> tag")
            
        for a_i in anchor_info:
            href = a_i["href"]
            if href.startswith("http://") and "doi.org" in href:
                formatting_issues.append(f"HTTP DOI URL (should be HTTPS): {href}")
                
        # Extract DOIs from hrefs and text
        extracted_dois = []
        for a_i in anchor_info:
            href = a_i["href"]
            m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', href)
            if m:
                extracted_dois.append(m.group(0).rstrip('.,;)'))
                
        plain_dois = re.findall(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
        for pd in plain_dois:
            pd_clean = pd.rstrip('.,;)')
            if pd_clean not in extracted_dois:
                extracted_dois.append(pd_clean)
                formatting_issues.append(f"Plain text DOI ({pd_clean}) not properly wrapped in anchor href")
                
        doi_status = "NONE"
        doi_issues = []
        existing_doi = extracted_dois[0] if extracted_dois else None
        cr_doi_info = None
        
        if existing_doi:
            cr_doi_info = query_crossref_doi(existing_doi)
            if not cr_doi_info.get("valid"):
                doi_status = "BROKEN_HTTP"
                doi_issues.append(f"Existing DOI ({existing_doi}) returned HTTP {cr_doi_info.get('status', cr_doi_info.get('error'))}")
            else:
                cr_title = cr_doi_info.get("title", "")
                words_doi_title = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', cr_title)]
                words_ref_text = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', text)]
                stop = {"journal", "study", "analysis", "review", "research", "effect", "effects", "human", "using", "between", "characterization"}
                common = set(words_doi_title).intersection(set(words_ref_text)) - stop
                
                if len(words_doi_title) > 3 and len(common) < 2:
                    doi_status = "HALLUCINATED"
                    doi_issues.append(f"HALLUCINATED DOI: {existing_doi} resolves to '{cr_title}', which does NOT match reference text '{text[:100]}...'")
                else:
                    doi_status = "OK"
        else:
            doi_status = "MISSING"
            doi_issues.append("No DOI present in reference")
            
        # Search CrossRef for true/suggested DOI
        suggested_doi = None
        search_cands = []
        if doi_status in ["MISSING", "BROKEN_HTTP", "HALLUCINATED"]:
            search_cands = query_crossref_search(text)
            if search_cands:
                top = search_cands[0]
                cand_title = top.get("title", "")
                cand_doi = top.get("doi", "")
                w_cand = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', cand_title)]
                w_ref = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', text)]
                stop = {"journal", "study", "analysis", "review", "research", "effect", "effects", "human", "using", "between", "characterization"}
                common_cand = set(w_cand).intersection(set(w_ref)) - stop
                if len(common_cand) >= 2 or (len(w_cand) > 0 and len(common_cand) >= len(w_cand)*0.4):
                    suggested_doi = f"https://doi.org/{cand_doi}"
                    
        ch_result["references"].append({
            "index": idx,
            "text": text,
            "raw_html": raw_html,
            "anchor_tags": anchor_info,
            "formatting_issues": formatting_issues,
            "existing_doi": existing_doi,
            "doi_status": doi_status,
            "doi_issues": doi_issues,
            "crossref_doi_info": cr_doi_info,
            "suggested_doi": suggested_doi,
            "search_candidates": search_cands
        })
        time.sleep(0.1)
        
    all_chapters_audit[ch_file] = ch_result

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\full_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(all_chapters_audit, f, indent=2)

print("\nFull chapter audit completed!")
