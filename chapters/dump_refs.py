import os
from bs4 import BeautifulSoup

chapters = [f"chapter_{i}.html" for i in range(60, 69)]

with open("manual_check.txt", "w", encoding="utf-8") as out:
    for ch in chapters:
        out.write(f"--- {ch} ---\n")
        try:
            with open(ch, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
        except Exception as e:
            out.write(f"Error: {e}\n\n")
            continue
            
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'span'])
        ref_heading = None
        for h in reversed(headings):
            text = h.get_text().lower()
            if 'reference' in text or 'structure-activity relationship' in text:
                ref_heading = h
                break
        
        ols = soup.find_all('ol')
        refs_elements = []
        if ols:
            refs_elements = ols[-1].find_all('li')
            
        if not refs_elements and ref_heading:
            curr = ref_heading.find_parent('p') if ref_heading.name in ['strong', 'span'] else ref_heading
            if curr:
                for sibling in curr.find_next_siblings():
                    if sibling.name == 'p' or sibling.name == 'li':
                        refs_elements.append(sibling)
        
        for i, el in enumerate(refs_elements):
            out.write(f"[{i+1}] {el}\n")
        out.write("\n")
