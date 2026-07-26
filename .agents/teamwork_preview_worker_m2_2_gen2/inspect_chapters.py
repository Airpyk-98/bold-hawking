import os
import glob
import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

chapters = [f'chapters/chapter_{i:02d}.html' for i in range(8, 15)]

for filepath in chapters:
    print('========================================')
    print('FILE:', filepath)
    if not os.path.exists(filepath):
        print('FILE NOT FOUND!')
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Find references heading
    headings = soup.find_all(lambda tag: tag.name in ['h1','h2','h3','h4','p','span','strong'] and 'references' in tag.get_text().lower())
    print('Headings found:', [h.get_text().strip() for h in headings[:3]])
    
    # Check ol/li
    ols = soup.find_all('ol')
    print('OL count:', len(ols))
    for idx, ol in enumerate(ols):
        lis = ol.find_all('li')
        print(f'  OL #{idx+1} has {len(lis)} LIs')

    # Check for <p> list items under references (like chapter 11)
    p_tags = soup.find_all('p')
    numbered_p = [p for p in p_tags if re.match(r'^\s*\d+\.\s+', p.get_text())]
    print('Numbered <p> tags count:', len(numbered_p))
        
    # Check for nested <a> tags
    nested_a = re.findall(r'<a\s+[^>]*>\s*<a\s+[^>]*>.*?</a>\s*</a>', html, re.DOTALL | re.IGNORECASE)
    print('Nested <a> tags count:', len(nested_a))
    
    # Check malformed href
    malformed_href = re.findall(r'href=["\']&lt;a\s+href=.*?', html, re.IGNORECASE)
    print('Malformed href count:', len(malformed_href))
