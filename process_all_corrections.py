import os
import sys
import re
from bs4 import BeautifulSoup, Tag

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

def fix_chapter_01():
    filepath = os.path.join(BASE_DIR, "chapter_01.html")
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    if not ols:
        print("Ch1: No <ol> found")
        return
    
    ref_ol = ols[0]
    for li in ref_ol.find_all("li"):
        # Fix unnesting
        clean_nesting(li)
        
        # Check Ref 4 DOI
        text = li.get_text()
        if "Turner" in text and "Croom" in text:
            for a in li.find_all("a"):
                a['href'] = "https://doi.org/10.1890/1051-0761(2000)010[0539:TEKAWI]2.0.CO;2"
                a.string = "https://doi.org/10.1890/1051-0761(2000)010[0539:TEKAWI]2.0.CO;2"
                
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Ch1 updated successfully.")

def fix_chapter_02():
    filepath = os.path.join(BASE_DIR, "chapter_02.html")
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    ref_ol = None
    for ol in ols:
        if len(ol.find_all("li", recursive=False)) == 18:
            ref_ol = ol
            break
            
    if ref_ol:
        for li in ref_ol.find_all("li", recursive=False):
            clean_nesting(li)
            clean_doi_links(li)
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Ch2 updated successfully.")

def fix_chapter_03():
    filepath = os.path.join(BASE_DIR, "chapter_03.html")
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    if ols:
        ref_ol = ols[0]
        for idx, li in enumerate(ref_ol.find_all("li", recursive=False), 1):
            clean_nesting(li)
            
            # Specific broken DOI fixes
            if idx == 2: # Ref 2: broken 8817078
                for a in li.find_all("a"):
                    if "8817078" in a.get('href', ''):
                        a.unwrap()
            elif idx == 8: # Ref 8: 10.1021/jf0301506 -> 10.1021/jf0301910
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1021/jf0301910"
                    a.string = "https://doi.org/10.1021/jf0301910"
            elif idx == 10: # Ref 10: S0944-7113(96
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1016/s0944-7113(96)80081-x"
                    a.string = "https://doi.org/10.1016/s0944-7113(96)80081-x"
            elif idx == 12: # Ref 12: 0308-8146(81
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1016/0308-8146(81)90019-4"
                    a.string = "https://doi.org/10.1016/0308-8146(81)90019-4"
            elif idx == 16: # Ref 16: 978-1-4899-1382-9_9 -> 978-1-4613-0413-5_9
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1007/978-1-4613-0413-5_9"
                    a.string = "https://doi.org/10.1007/978-1-4613-0413-5_9"
            else:
                clean_doi_links(li)
                
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Ch3 updated successfully.")

def fix_chapter_05():
    filepath = os.path.join(BASE_DIR, "chapter_05.html")
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # Find reference heading
    ref_head = None
    for h in soup.find_all(['p', 'h2', 'h3']):
        if 'reference' in h.get_text().lower():
            ref_head = h
            break
            
    if not ref_head:
        print("Ch5: Reference heading not found!")
        return

    # Create <h2>References</h2>
    h2_tag = soup.new_tag("h2")
    h2_tag.string = "References"
    
    # Collect all 20 reference paragraphs
    ref_paras = []
    curr = ref_head.find_next_sibling()
    while curr:
        next_sibling = curr.find_next_sibling()
        if curr.name == 'p':
            text = curr.get_text().strip()
            if text and (re.match(r'^\d+[\.\)]', text) or len(ref_paras) < 20):
                ref_paras.append(curr)
        curr = next_sibling
        
    print(f"Ch5: Found {len(ref_paras)} reference paragraphs to convert.")
    
    # Create <ol> element
    ol_tag = soup.new_tag("ol")
    
    for idx, p in enumerate(ref_paras, 1):
        li_tag = soup.new_tag("li")
        # Clean paragraph contents: remove leading "1. ", "2. ", etc.
        # Move children of p into li
        p_html = str(p)
        # Clean nested a
        sub_soup = BeautifulSoup(p_html, 'html.parser')
        p_elem = sub_soup.p if sub_soup.p else sub_soup
        clean_nesting(p_elem)
        clean_doi_links(p_elem)
        
        # Specific fixes for Ch 5
        if idx == 14: # Ref 14: truncated 0968-0896(99
            for a in p_elem.find_all("a"):
                a['href'] = "https://doi.org/10.1016/s0968-0896(99)00234-5"
                a.string = "https://doi.org/10.1016/s0968-0896(99)00234-5"
        elif idx == 15: # Ref 15: splitrock URL
            for a in p_elem.find_all("a"):
                a['href'] = "https://splitrockenvironmental.ca/products/arnica-salve?variant=33785190383675"
                a.string = "https://splitrockenvironmental.ca/products/arnica-salve?variant=33785190383675"
                
        # Remove leading "1. ", "2. ", etc from text if present
        # In BeautifulSoup, we can clean the first NavigableString
        first_child = p_elem.contents[0] if p_elem.contents else None
        if first_child and isinstance(first_child, str):
            cleaned_str = re.sub(r'^\d+[\.\)]\s*', '', first_child)
            first_child.replace_with(cleaned_str)
            
        li_tag.extend(p_elem.contents)
        ol_tag.append(li_tag)
        
    # Replace ref_head and ref_paras with h2_tag and ol_tag
    ref_head.replace_with(h2_tag)
    h2_tag.insert_after(ol_tag)
    
    for p in ref_paras:
        p.decompose()
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Ch5 updated and converted to <ol> list successfully.")

def fix_chapter_06():
    filepath = os.path.join(BASE_DIR, "chapter_06.html")
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    ref_ol = None
    for ol in ols:
        if len(ol.find_all("li", recursive=False)) == 9:
            ref_ol = ol
            break
            
    if ref_ol:
        for idx, li in enumerate(ref_ol.find_all("li", recursive=False), 1):
            clean_nesting(li)
            
            # Specific fixes for truncated DOIs in Ch6
            if idx == 5:
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1016/s0031-9422(00)84838-4"
                    a.string = "https://doi.org/10.1016/s0031-9422(00)84838-4"
            elif idx == 6:
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1016/s0031-9422(00)97369-2"
                    a.string = "https://doi.org/10.1016/s0031-9422(00)97369-2"
            elif idx == 8:
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1016/0031-9422(91)83426-l"
                    a.string = "https://doi.org/10.1016/0031-9422(91)83426-l"
            elif idx == 9:
                for a in li.find_all("a"):
                    a['href'] = "https://doi.org/10.1016/s0049-3848(03)00379-7"
                    a.string = "https://doi.org/10.1016/s0049-3848(03)00379-7"
            else:
                clean_doi_links(li)
                
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Ch6 updated successfully.")

def fix_chapter_07():
    filepath = os.path.join(BASE_DIR, "chapter_07.html")
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    ref_ol = None
    for ol in ols:
        if len(ol.find_all("li", recursive=False)) == 14:
            ref_ol = ol
            break
            
    if ref_ol:
        for li in ref_ol.find_all("li", recursive=False):
            clean_nesting(li)
            clean_doi_links(li)
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Ch7 updated successfully.")

def clean_nesting(elem):
    for outer_a in elem.find_all('a'):
        inner_a = outer_a.find('a')
        if inner_a:
            outer_a.replace_with(inner_a)

def clean_doi_links(elem):
    for a in elem.find_all('a'):
        href = a.get('href', '')
        if 'doi.org/' in href or href.startswith('10.'):
            doi_match = re.search(r'10\.\d{4,9}/[^\s"<>\)]+', href)
            if doi_match:
                clean_doi = doi_match.group(0).rstrip('.\'")>]')
                a['href'] = f"https://doi.org/{clean_doi}"
                a.string = f"https://doi.org/{clean_doi}"

if __name__ == "__main__":
    fix_chapter_01()
    fix_chapter_02()
    fix_chapter_03()
    fix_chapter_05()
    fix_chapter_06()
    fix_chapter_07()
