import os
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\extracted_raw.json", "r", encoding="utf-8") as f:
    chapters_data = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
crossref_headers = {'User-Agent': 'mailto:explorer@example.com'}

def check_doi_http(doi_url):
    url = doi_url if doi_url.startswith("http") else f"https://doi.org/{doi_url}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), resp.geturl()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e), None

def query_crossref_doi(doi):
    # Strip url prefix if present
    clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi).strip()
    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
    req = urllib.request.Request(url, headers=crossref_headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            message = data.get('message', {})
            title = message.get('title', [''])[0]
            authors = []
            for a in message.get('author', []):
                authors.append(f"{a.get('given', '')} {a.get('family', '')}".strip())
            year = None
            published = message.get('published-print') or message.get('published-online') or message.get('issued')
            if published and 'date-parts' in published and published['date-parts']:
                year = published['date-parts'][0][0]
            return {
                "valid": True,
                "title": title,
                "authors": authors,
                "year": year,
                "doi": clean_doi
            }
    except urllib.error.HTTPError as e:
        return {"valid": False, "status": e.code, "doi": clean_doi}
    except Exception as e:
        return {"valid": False, "error": str(e), "doi": clean_doi}

def query_crossref_search(text):
    # Remove URLs/DOIs from search text
    clean_text = re.sub(r'https?://[^\s]+', '', text)
    clean_text = re.sub(r'doi:[^\s]+', '', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'\[.*?\]', '', clean_text)
    clean_text = clean_text.strip()
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(clean_text[:250])}&rows=3"
    req = urllib.request.Request(url, headers=crossref_headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                t = item.get('title', [''])[0]
                d = item.get('DOI', '')
                y = None
                published = item.get('published-print') or item.get('published-online') or item.get('issued')
                if published and 'date-parts' in published and published['date-parts']:
                    y = published['date-parts'][0][0]
                results.append({'title': t, 'doi': d, 'year': y})
            return results
    except Exception as e:
        return []

analyzed_output = {}

for ch_file, ch_info in chapters_data.items():
    print(f"\nProcessing {ch_file} ({ch_info['total_references']} references)...")
    ch_analysis = {
        "file": ch_file,
        "refs_header_text": ch_info["refs_header_text"],
        "total_references": ch_info["total_references"],
        "items": []
    }
    
    for ref in ch_info["references"]:
        idx = ref["index"]
        text = ref["text"]
        raw_html = ref["raw_html"]
        anchor_tags = ref["anchor_tags"]
        
        item_analysis = {
            "index": idx,
            "text": text,
            "raw_html": raw_html,
            "anchor_tags": anchor_tags,
            "formatting_issues": [],
            "doi_issues": [],
            "existing_doi": None,
            "crossref_match_for_existing_doi": None,
            "crossref_search_candidates": [],
            "suggested_doi": None,
            "doi_status": "NONE" # NONE, OK, MALFORMED_TAG, BROKEN_HTTP, HALLUCINATED, MISSING
        }
        
        # Check formatting & malformed HTML tags
        # 1. Unclosed anchor tag or bad href
        for a in anchor_tags:
            href = a["href"]
            raw_a = a["raw_a_tag"]
            if not href:
                item_analysis["formatting_issues"].append("Anchor tag has empty href")
            elif href.startswith("http://") and "doi.org" in href:
                item_analysis["formatting_issues"].append(f"HTTP DOI link (should be HTTPS): {href}")
            elif not href.startswith("http://") and not href.startswith("https://"):
                item_analysis["formatting_issues"].append(f"Non-standard href scheme: {href}")
        
        if "<a>" in raw_html and "</a>" not in raw_html:
            item_analysis["formatting_issues"].append("Unclosed <a> tag detected in HTML")
            
        # Extract existing DOIs from anchor tags or plain text
        existing_dois = []
        for a in anchor_tags:
            href = a["href"]
            doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', href)
            if doi_match:
                existing_dois.append(doi_match.group(0).rstrip('.,;)'))
        
        # Also check plain text DOIs
        plain_dois = ref.get("plain_dois_in_text", [])
        for pd in plain_dois:
            pd_clean = pd.rstrip('.,;)')
            if pd_clean not in existing_dois:
                existing_dois.append(pd_clean)
                if not anchor_tags:
                    item_analysis["formatting_issues"].append(f"Plain text DOI detected without <a> tag: {pd_clean}")
                else:
                    item_analysis["formatting_issues"].append(f"DOI in text ({pd_clean}) not wrapped in href anchor tag")
        
        if existing_dois:
            primary_doi = existing_dois[0]
            item_analysis["existing_doi"] = primary_doi
            
            # Query CrossRef for this DOI
            cr_doi_info = query_crossref_doi(primary_doi)
            item_analysis["crossref_match_for_existing_doi"] = cr_doi_info
            
            if not cr_doi_info.get("valid"):
                item_analysis["doi_issues"].append(f"DOI {primary_doi} returned HTTP {cr_doi_info.get('status', cr_doi_info.get('error'))} from CrossRef API")
                item_analysis["doi_status"] = "BROKEN_HTTP"
            else:
                # Check if the title returned by CrossRef matches the reference text
                doi_title = cr_doi_info.get("title", "")
                # Simple keyword check between doi_title and reference text
                words_doi_title = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', doi_title)]
                words_ref_text = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', text)]
                
                common_words = set(words_doi_title).intersection(set(words_ref_text))
                # Exclude ultra-common words
                stop_words = {"journal", "study", "analysis", "review", "research", "effect", "effects", "human", "using", "between", "characterization"}
                common_words_filtered = common_words - stop_words
                
                if len(common_words_filtered) < 2 and len(words_doi_title) > 3:
                    item_analysis["doi_issues"].append(f"POTENTIAL HALLUCINATED DOI: DOI {primary_doi} resolves to '{doi_title}', which does NOT match reference text '{text[:120]}...'")
                    item_analysis["doi_status"] = "HALLUCINATED"
                else:
                    item_analysis["doi_status"] = "OK"
        else:
            item_analysis["doi_status"] = "MISSING"
            item_analysis["doi_issues"].append("No DOI found in anchor tags or text.")
            
        # Now query CrossRef search to find the correct/actual DOI for the paper title
        search_results = query_crossref_search(text)
        item_analysis["crossref_search_candidates"] = search_results
        if search_results:
            top_cand = search_results[0]
            cand_title = top_cand.get("title", "")
            cand_doi = top_cand.get("doi", "")
            
            # Check overlap with ref text
            words_cand_title = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', cand_title)]
            words_ref_text = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', text)]
            common_cand = set(words_cand_title).intersection(set(words_ref_text)) - {"journal", "study", "analysis", "review", "research", "effect", "effects", "human", "using", "between", "characterization"}
            
            if len(common_cand) >= 2 or (len(words_cand_title) > 0 and len(common_cand) >= len(words_cand_title)*0.5):
                item_analysis["suggested_doi"] = f"https://doi.org/{cand_doi}"
        
        ch_analysis["items"].append(item_analysis)
        time.sleep(0.1) # avoid overwhelming crossref API
        
    analyzed_output[ch_file] = ch_analysis

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\verification_results.json", "w", encoding="utf-8") as f:
    json.dump(analyzed_output, f, indent=2)

print("\nFinished verification and CrossRef analysis for Chapters 8-14!")
