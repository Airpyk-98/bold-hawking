from bs4 import BeautifulSoup
import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

chapters = soup.find_all(class_='chapter')
print(f"Found {len(chapters)} elements with class 'chapter'")

if len(chapters) == 0:
    sections = soup.find_all('section')
    print(f"Found {len(sections)} sections")
    for s in sections[:5]:
        print(s.get('class'), s.get('id'))
else:
    for c in chapters[:5]:
        print(c.name, c.get('class'))
