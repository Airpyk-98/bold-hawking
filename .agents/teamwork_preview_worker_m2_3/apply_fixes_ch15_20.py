import os
import re
from bs4 import BeautifulSoup

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

# Exact DOI replacements dictionary: (chapter, ref_num) -> (old_doi_substring, new_doi)
doi_replacements = {
    (15, 3): ("10.1080/13693780400029112", "10.1080/13693780400004810"),
    (15, 5): ("10.1007/BF00973171", "10.1007/bf00973103"),
    (15, 9): ("10.1016/j.phymed.2010.01.013", "10.1016/j.phymed.2009.10.002"),
    (15, 12): ("10.1186/s12906-016-1131-8", "10.1186/s12906-016-1128-7"),
    (15, 13): ("10.1078/0944-7113-00258", "10.1078/094471102321621322"),
    (15, 14): ("10.1016/j.ejphar.2003.11.010", "10.1016/j.ejphar.2003.11.066"),
    (17, 6): ("10.1007/s11101-020-09701-z", "10.1007/s11101-020-09671-y"),
    (20, 9): ("10.1016/j.jfoodeng.2004.08.024", "10.1016/j.jfoodeng.2004.08.032"),
}

def clean_li_anchors(li):
    # Find all anchor tags
    a_tags = li.find_all("a")
    if not a_tags:
        return
    
    # We want to extract the ultimate target URL text
    # Usually the innermost anchor or first anchor has the clean link URL
    # Let's inspect hrefs
    target_href = None
    for a in a_tags:
        h = a.get("href")
        if h:
            target_href = h
            break
            
    if not target_href:
        return

    # Check if we have DOI replacement for this target_href
    # Reconstruct clean anchor tag
    new_a = li.find_all("a")[-1] # or inner anchor
    inner_text = a_tags[-1].get_text(strip=True) if a_tags else target_href
    
    # Remove all nested anchor tags and replace with single clean anchor tag
    # First, decompose all existing <a> tags inside li
    # Save the structure of li before <a> tag
    li_str = str(li)
    
    # Simple regex unwrapping approach to avoid BeautifulSoup mutating text around tags awkwardly:
    # Pattern: <a href="([^"]+)">\s*<a href="([^"]+)">([^<]+)</a>\s*</a>
    pattern = re.compile(r'<a\s+href="([^"]+)">\s*<a\s+href="([^"]+)">([\s\S]*?)</a>\s*</a>', re.IGNORECASE)
    
    def repl(m):
        outer_href = m.group(1)
        inner_href = m.group(2)
        link_content = m.group(3).strip()
        
        # Pick the best href (if outer had typo like SICI case typo, use inner_href)
        chosen_href = inner_href if "SICI" in inner_href or "sici" in inner_href else (inner_href or outer_href)
        return f'<a href="{chosen_href}">{link_content}</a>'
        
    cleaned_str = pattern.sub(repl, li_str)
    return cleaned_str

for ch in range(15, 21):
    fname = f"chapter_{ch}.html"
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    ols = soup.find_all("ol")
    if not ols:
        print(f"Skipping {fname}: No <ol> found")
        continue
        
    ol = ols[-1]
    lis = ol.find_all("li", recursive=False)
    
    for idx, li in enumerate(lis, 1):
        # 1. Check DOI replacements
        if (ch, idx) in doi_replacements:
            old_doi, new_doi = doi_replacements[(ch, idx)]
            # Update in raw li HTML string
            li_html = str(li)
            li_html = li_html.replace(old_doi, new_doi)
            li.replace_with(BeautifulSoup(li_html, "html.parser"))
            
    # Re-fetch lis after replacements
    lis = ol.find_all("li", recursive=False)
    
    # 2. Fix Chapter 15 Ref 10 SICI case typo if present
    if ch == 15 and len(lis) >= 10:
        ref10_html = str(lis[9])
        # Replace lowercase sici with uppercase SICI if needed
        ref10_html = ref10_html.replace("(sici)1099-1573(199909)13:6&lt;540::aid-ptr523&gt;3.0.co;2-i", "(SICI)1099-1573(199909)13:6&lt;540::AID-PTR523&gt;3.0.CO;2-J")
        ref10_html = ref10_html.replace("(sici)1099-1573(199909)13:6<540::aid-ptr523>3.0.co;2-i", "(SICI)1099-1573(199909)13:6<540::AID-PTR523>3.0.CO;2-J")
        lis[9].replace_with(BeautifulSoup(ref10_html, "html.parser"))

    # 3. Fix Chapter 20 specific items
    if ch == 20:
        lis = ol.find_all("li", recursive=False)
        for idx, li in enumerate(lis, 1):
            li_html = str(li)
            # Strip hardcoded leading number like <li> 1. or <li>1. or <li>  12.
            li_html = re.sub(r'(<li[^>]*>)\s*\d+\.\s*', r'\1', li_html)
            
            # Ref 4 truncated text fix
            if idx == 4:
                if "Oral teachings and traditional knowledge" not in li_html:
                    li_html = re.sub(r'Elders and Community members of the Cayoose Creek Band of Sekw[’\']el[’\']was\.\s*',
                                     r'Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.). <em>Oral teachings and traditional knowledge</em>. ',
                                     li_html)
            
            # Ref 2 missing link fix
            if idx == 2:
                if "aafp.org" not in li_html and "<a " not in li_html:
                    li_html = li_html.replace("465–468.", '465–468. <a href="https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html">https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html</a>')
                    li_html = li_html.replace("465468.", '465–468. <a href="https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html">https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html</a>')

            li.replace_with(BeautifulSoup(li_html, "html.parser"))

    # 4. Clean up all nested <a> tags across the entire <ol>
    ol_html = str(ol)
    nested_pattern = re.compile(r'<a\s+href="([^"]+)">\s*<a\s+href="([^"]+)">([\s\S]*?)</a>\s*</a>', re.IGNORECASE)

    while nested_pattern.search(ol_html):
        ol_html = nested_pattern.sub(r'<a href="\2">\3</a>', ol_html)

    # Replace <ol> in soup with cleaned ol
    new_ol = BeautifulSoup(ol_html, "html.parser")
    ol.replace_with(new_ol)

    # Save modified HTML back to file with UTF-8 encoding
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(str(soup))
        
    print(f"Successfully processed and updated {fname}")

