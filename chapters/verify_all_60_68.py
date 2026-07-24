import os
import re
import json
import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import time

def search_crossref(title):
    try:
        url = "https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(title) + "&rows=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:audit@example.com'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            items = data.get('message', {}).get('items', [])
            if items:
                return "https://doi.org/" + items[0]['DOI']
    except Exception as e:
        pass
    return None

def check_doi(doi_url):
    # doi_url usually https://doi.org/10.xxxx/...
    try:
        req = urllib.request.Request(doi_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return True, "OK"
    except HTTPError as e:
        if e.code in [403, 405]:
            return True, "Bot Block" # Publisher blocked, likely OK
        elif e.code == 404:
            return False, "404 Not Found"
        else:
            return False, f"HTTP {e.code}"
    except URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)

report = []

for i in range(60, 69):
    fname = f'chapter_{i:02d}.html'
    if not os.path.exists(fname): continue
    
    with open(fname, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    ref_heading = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong', 'span'] and tag.get_text() and ('References' in tag.get_text().strip() or 'Structure-Activity' in tag.get_text().strip()))
    
    if not ref_heading:
        continue
        
    # Get all tags after heading that might be references
    refs = []
    # If the next sibling is an ol, grab its lis
    nxt = ref_heading.find_next_sibling()
    while nxt:
        if nxt.name in ['ol', 'ul']:
            refs.extend(nxt.find_all('li'))
            break
        elif nxt.name == 'p' and re.match(r'^\d+\.', nxt.get_text().strip()):
            refs.append(nxt)
            nxt = nxt.find_next_sibling()
        elif nxt.name == 'p' and not nxt.get_text().strip():
            nxt = nxt.find_next_sibling()
        else:
            # Check if there are p tags that are references
            break
            
    if not refs:
        # Fallback to finding all p tags that start with number. after the heading
        for p in ref_heading.find_all_next('p'):
            text = p.get_text().strip()
            if re.match(r'^\d+\.', text):
                refs.append(p)
                
    for ref in refs:
        html_str = str(ref)
        text = ref.get_text().strip()
        
        # Check plain text DOIs or URLs
        # Find anything that looks like a DOI: 10.xxxx/...
        doi_matches = set(re.findall(r'(10\.\d{4,9}/[-._;()/:A-Z0-9a-z]+)', text))
        # Find anything that looks like http:
        url_matches = set(re.findall(r'(https?://[^\s<]+)', text))
        
        anchors = ref.find_all('a')
        linked_urls = [a.get('href') for a in anchors if a.get('href')]
        
        errors = []
        corrections = []
        
        # Are there plain text links/DOIs not in a tags?
        for d in doi_matches:
            # if this DOI string is not inside any href, it's plain text
            if not any(d in href for href in linked_urls):
                errors.append(f"Unclickable plain text link ({d})")
                corrections.append(f"Wrap in <a href=\"https://doi.org/{d}\">https://doi.org/{d}</a>")
                
        for u in url_matches:
            # clean trailing punct
            u = u.rstrip('.,;)')
            if not any(u in href for href in linked_urls) and "doi.org" not in u: # handle doi separately
                errors.append(f"Unclickable plain text link ({u})")
                corrections.append(f"Wrap in <a href=\"{u}\">{u}</a>")
            elif not any(u in href for href in linked_urls) and "doi.org" in u:
                errors.append(f"Unclickable plain text link ({u})")
                corrections.append(f"Wrap in <a href=\"{u}\">{u}</a>")
                
        # Check validity of ALL DOIs found
        all_dois = []
        for href in linked_urls:
            if 'doi.org/' in href:
                all_dois.append(href)
        for d in doi_matches:
            if not any(d in d_href for d_href in all_dois):
                all_dois.append(f"https://doi.org/{d}")
                
        for d_url in all_dois:
            if '10.2307/' in d_url:
                errors.append(f"Old JSTOR handle ({d_url})")
                # Need to use crossref to find real DOI
                real_doi = search_crossref(text)
                if real_doi:
                    corrections.append(f"Replace JSTOR handle with {real_doi}")
                else:
                    corrections.append(f"Could not resolve JSTOR handle, please find valid DOI")
            else:
                ok, msg = check_doi(d_url)
                if not ok:
                    if "404" in msg:
                        errors.append(f"Broken DOI ({d_url}) - 404 Not Found")
                        real_doi = search_crossref(text)
                        if real_doi:
                            corrections.append(f"Replace DOI with {real_doi}")
                        else:
                            corrections.append(f"Find universally accepted DOI via CrossRef")
                    else:
                        errors.append(f"Broken DOI ({d_url}) - {msg}")
                        corrections.append(f"Check and replace DOI")
        
        if ref.name == 'p':
            errors.append("Reference is in a <p> tag instead of an <ol> <li> item.")
            corrections.append("Wrap reference in <li> and place within an <ol> list.")
            
        if errors:
            report.append({
                'chapter': fname,
                'text': text,
                'errors': errors,
                'corrections': corrections
            })

with open('audit_report_60_68.json', 'w', encoding='utf-8') as out:
    json.dump(report, out, indent=2, ensure_ascii=False)
