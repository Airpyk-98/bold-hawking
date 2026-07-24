import os
import re
from bs4 import BeautifulSoup

for i in range(60, 69):
    fname = f'chapter_{i:02d}.html'
    if not os.path.exists(fname): continue
    
    print(f'\\n==== {fname} ====')
    with open(fname, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Search for heading containing 'References'
    ref_heading = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'strong', 'span'] and tag.get_text() and 'References' in tag.get_text().strip())
    
    if not ref_heading:
        print('No references heading found.')
        continue
    
    # Try to find the associated ol
    curr = ref_heading
    ol = None
    while curr:
        if curr.name == 'ol' or curr.name == 'ul':
            ol = curr
            break
        nxt = curr.find_next_sibling()
        if nxt:
            if nxt.name == 'ol' or nxt.name == 'ul':
                ol = nxt
                break
            else:
                curr = nxt
        else:
            if curr.parent:
                curr = curr.parent.find_next_sibling()
            else:
                break
    
    if not ol:
        print('No ol found after references heading. Checking paragraphs...')
        # Look at p tags following
        ps = ref_heading.find_all_next('p')
        for j, p in enumerate(ps[:15], 1):
            text = str(p)
            print(f'P[{j}]: {text}')
        continue
    
    for j, li in enumerate(ol.find_all('li', recursive=False), 1):
        html_str = str(li)
        # Check for anchors
        anchors = li.find_all('a')
        
        # Check for plain text URLs or DOIs
        # regex for url: https?://[^\s<]+
        # regex for doi: 10\.\d{4,9}/[-._;()/:A-Z0-9]+i
        
        plain_text_candidates = li.get_text()
        
        print(f'[{j}] HTML: {html_str}')
        for a in anchors:
            print(f'   Found LINK: {a["href"]}')
