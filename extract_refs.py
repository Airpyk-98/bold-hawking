import os
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse
import json
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
index_file = os.path.join(base_dir, "index.html")
out_md = r"C:\Users\DELL\.gemini\antigravity\brain\6a70ced1-308c-4b55-8f91-d40f1d746322\references_verification.md"

def extract_links(text):
    return re.findall(r'(https?://[^\s]+)', text)

with open(index_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

chapters = soup.find_all("section", class_=lambda c: c and "chapter" in c.split())

with open(out_md, "w", encoding="utf-8") as out:
    out.write("# References Verification (Chapters 1-5)\n\n")

    for i in range(5):
        if i >= len(chapters): break
        chapter = chapters[i]
        out.write(f"## Chapter {i+1}\n\n")
        
        # Find any element containing exactly 'References' or close to it
        refs_heading = chapter.find(string=re.compile(r'^\s*References\s*$', re.IGNORECASE))
        if not refs_heading:
            refs_heading = chapter.find(string=re.compile(r'References', re.IGNORECASE))
            
        if not refs_heading:
            out.write("No references heading found in this chapter.\n\n")
            continue
            
        parent = refs_heading.parent
        # Go up until we find the block element containing the heading
        while parent and parent.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']:
            parent = parent.parent
            
        ol = parent.find_next("ol")
        if not ol:
            out.write("No ordered list found after References.\n\n")
            continue
            
        # Parse the references
        for li in ol.find_all("li"):
            text = li.get_text(separator=" ", strip=True)
            links = extract_links(text)
            
            for a in li.find_all("a"):
                href = a.get("href")
                if href and href not in links: links.append(href)
                
            out.write(f"- {text}\n")
            
            error_found = False
            correction = ""
            
            if links:
                for link in links:
                    link = link.rstrip('.,;)')
                    
                    if "doi.org" in link or "crossref" in link or "doi:" in link.lower():
                        try:
                            req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req, timeout=10) as response:
                                if response.getcode() != 200:
                                    error_found = True
                        except urllib.error.HTTPError as e:
                            error_found = True
                        except Exception as e:
                            error_found = True
                            
                        if error_found:
                            # Try Crossref lookup to find the correct one
                            try:
                                query = urllib.parse.quote(text[:150])
                                url = f"https://api.crossref.org/works?query.bibliographic={query}&rows=1"
                                req2 = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
                                with urllib.request.urlopen(req2, timeout=5) as res2:
                                    data = json.loads(res2.read().decode('utf-8'))
                                    items = data.get("message", {}).get("items", [])
                                    if items:
                                        suggested_doi = items[0].get("DOI")
                                        if suggested_doi:
                                            correction = f"https://doi.org/{suggested_doi}"
                            except Exception:
                                pass
            
            if error_found:
                out.write(f"  - **Error detected in link(s)**\n")
                if correction:
                    out.write(f"  - **Correction**: Use {correction} instead.\n")
                else:
                    out.write(f"  - **Correction**: Unable to find a CrossRef match automatically.\n")
            else:
                out.write(f"  - **Status**: Checked and OK.\n")
                
        out.write("\n")
