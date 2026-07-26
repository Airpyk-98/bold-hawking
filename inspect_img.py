from bs4 import BeautifulSoup
import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

chapters = soup.find_all(class_='chapter')
ch19 = chapters[18] # Chapter 19
imgs = ch19.find_all('img')
for i, img in enumerate(imgs[:2]):
    print(f"--- IMG {i} ---")
    print("IMG parent:", img.parent.name, img.parent.get('class'))
    # Print the next sibling or parent's next sibling
    parent = img.parent
    if parent.next_sibling:
        print("Next sibling:", repr(parent.next_sibling.text[:100]))
