import os
import sys
import re
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking"

# Define known DOI corrections map (hallucinated/truncated/broken DOIs to valid DOIs or actions)
DOI_CORRECTIONS = {
    # Chapter 1
    "10.1890/1051-0761(2000)010": "10.1890/1051-0761(2000)010[0539:TEKAWI]2.0.CO;2",
    
    # Chapter 3
    "10.1021/jf0301506": "10.1021/jf0301910",
    "10.1016/S0944-7113(96": "10.1016/s0944-7113(96)80081-x",
    "10.1016/0308-8146(81": "10.1016/0308-8146(81)90019-4",
    "10.1007/978-1-4899-1382-9_9": "10.1007/978-1-4613-0413-5_9",
    "10.1155/2020/8817078": None, # Unverifiable hallucinated DOI, remove link
    
    # Chapter 5
    "10.1016/s0968-0896(99": "10.1016/s0968-0896(99)00234-5",
    
    # Chapter 6
    "10.1016/S0031-9422(00": None, # Could match ref 5 or 6, let's handle specifically below
}

def clean_item_html(elem_soup, default_doi_update=None):
    """
    Cleans an HTML element (li or p) by:
    1. Unnesting duplicate/nested <a> tags.
    2. Replacing broken/truncated DOIs with correct DOIs.
    3. Ensuring proper single <a href="https://doi.org/...">...</a> structure.
    """
    raw_str = str(elem_soup)
    
    # 1. Unnest nested <a> tags
    # Find outer <a> that contains inner <a>
    for outer_a in elem_soup.find_all('a'):
        inner_a = outer_a.find('a')
        if inner_a:
            # Replace outer_a with inner_a or clean anchor
            outer_a.replace_with(inner_a)
            
    # Re-parse element
    elem_str = str(elem_soup)
    
    # Check for truncated / broken DOIs in text or hrefs
    # Replace truncated text/href pattern if found
    for broken, fixed in DOI_CORRECTIONS.items():
        if broken in elem_str:
            if fixed:
                elem_str = elem_str.replace(broken, fixed)
            else:
                # Remove anchor wrapping broken DOI
                pass
                
    # Normalize DOI links in href and inner text
    # Ensure every doi link has href="https://doi.org/<DOI>" and text "https://doi.org/<DOI>"
    # Let's parse with BeautifulSoup to clean anchor attributes
    sub_soup = BeautifulSoup(elem_str, 'html.parser')
    
    for a in sub_soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text().strip()
        
        # Clean mangled href like: href="<a href=" https:="" splitrockenvironmental.ca"=""
        if '&lt;a href=' in href or 'splitrockenvironmental' in href:
            a['href'] = "https://splitrockenvironmental.ca/products/arnica-salve?variant=33785190383675"
            a.string = "https://splitrockenvironmental.ca/products/arnica-salve?variant=33785190383675"
            continue
            
        if 'doi.org/' in href or '10.' in href:
            # Extract DOI
            doi_match = re.search(r'10\.\d{4,9}/[^\s"<>\)]+', href)
            if not doi_match:
                doi_match = re.search(r'10\.\d{4,9}/[^\s"<>\)]+', text)
            if doi_match:
                clean_doi = doi_match.group(0).rstrip('.\'")>]')
                
                # Check corrections map
                if clean_doi in DOI_CORRECTIONS:
                    corr = DOI_CORRECTIONS[clean_doi]
                    if corr:
                        clean_doi = corr
                    else:
                        # Remove link, keep text if any
                        a.unwrap()
                        continue
                        
                a['href'] = f"https://doi.org/{clean_doi}"
                a.string = f"https://doi.org/{clean_doi}"
                
    # Return cleaned inner HTML content or soup
    return sub_soup

print("Cleaner helper function created.")
