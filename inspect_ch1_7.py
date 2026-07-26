import os
import re
from bs4 import BeautifulSoup

def inspect_chapter(filepath):
    print(f"=== {filepath} ===")
    if not os.path.exists(filepath):
        print("File does not exist!")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find reference section
    # Heading can be h1, h2, h3, or p with strong "References"
    ref_heading = None
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p']):
        if 'reference' in h.get_text().lower():
            ref_heading = h
            print(f"Found heading: {h}")
            break
            
    # Find ol or lists
    ols = soup.find_all('ol')
    print(f"Total <ol> elements in document: {len(ols)}")
    
    # If chapter 5 or paragraph list
    ps = soup.find_all('p')
    print(f"Total <p> elements: {len(ps)}")
    
    # Extract references
    references = []
    if ols:
        # Check which OL is reference list (usually the last one or after reference heading)
        for idx, ol in enumerate(ols):
            items = ol.find_all('li')
            print(f"OL #{idx}: {len(items)} items")
            # print first item preview
            if items:
                print(f"  Item 1 preview: {items[0].get_text()[:80]}")
    else:
        print("No <ol> tags found in document!")
        
inspect_chapter("chapters/chapter_01.html")
inspect_chapter("chapters/chapter_02.html")
inspect_chapter("chapters/chapter_03.html")
inspect_chapter("chapters/chapter_04.html")
inspect_chapter("chapters/chapter_05.html")
inspect_chapter("chapters/chapter_06.html")
inspect_chapter("chapters/chapter_07.html")
