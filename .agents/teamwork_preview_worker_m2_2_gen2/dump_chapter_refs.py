import os
import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

chapters = [f'chapters/chapter_{i:02d}.html' for i in range(8, 15)]

for filepath in chapters:
    print('========================================')
    print('DUMPING REF SECTION FOR:', filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find the References section
    # Look for element with text 'References'
    ref_head = None
    for tag in soup.find_all(['h1','h2','h3','h4','p','span','strong']):
        if tag.get_text().strip().lower() == 'references':
            ref_head = tag
            # Find closest parent paragraph or div if span/strong
            while ref_head.name in ['span', 'strong']:
                ref_head = ref_head.parent
            break

    if ref_head:
        print("Found References heading:", ref_head)
        # Print siblings or container following ref_head
        curr = ref_head.next_sibling
        count = 0
        while curr and count < 30:
            if hasattr(curr, 'name') and curr.name:
                print(f"[{curr.name}]: {str(curr)[:300]}")
                count += 1
            curr = curr.next_sibling
    else:
        print("No References heading found!")
