import glob
from bs4 import BeautifulSoup
import re
import os

with open('audit_60_68_refs.txt', 'w', encoding='utf-8') as out:
    for i in range(60, 69):
        fname = f'chapter_{i:02d}.html'
        if not os.path.exists(fname): continue
        with open(fname, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # We need to find the specific References ordered list.
        # Let's search for headers that contain 'References'
        ref_header = soup.find(lambda tag: tag.name in ['h2', 'h3'] and 'References' in tag.get_text(strip=True))
        target_ol = None
        if ref_header:
            # find next sibling that is an ol
            nxt = ref_header.find_next_sibling()
            while nxt:
                if nxt.name == 'ol':
                    target_ol = nxt
                    break
                nxt = nxt.find_next_sibling()
        
        if not target_ol:
            # Fallback to the last ol in section
            section = soup.find('section', class_='chapter')
            if section:
                ols = section.find_all('ol')
                if ols: target_ol = ols[-1]
            if not target_ol:
                ols = soup.find_all('ol')
                if ols: target_ol = ols[-1]
                
        out.write(f'\n--- {fname} ---\n')
        if not target_ol:
            out.write('No <ol> found!\n')
            continue
        
        for j, li in enumerate(target_ol.find_all('li', recursive=False), 1):
            out.write(f'[{j}] {li}\n')
