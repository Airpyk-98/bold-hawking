import io
from bs4 import BeautifulSoup
import os
import re

os.makedirs('chapters', exist_ok=True)

with io.open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

chapters = soup.find_all(class_='chapter')
print(f"Splitting {len(chapters)} chapters...")

# To keep the main structure, we replace each chapter with a placeholder
for i, ch in enumerate(chapters, 1):
    # Determine actual chapter number from the span inside h1 if it exists
    h1 = ch.find('h1')
    chapter_num_str = str(i)
    if h1 and h1.find('span'):
        chapter_num_str = h1.find('span').text.strip()
        # Keep only digits just in case
        chapter_num_str = re.sub(r'\D', '', chapter_num_str)
        if not chapter_num_str:
            chapter_num_str = str(i)
    
    # Save the chapter to a file
    file_path = f'chapters/chapter_{i:02d}.html'
    

    with io.open(file_path, 'w', encoding='utf-8') as out_f:
        out_f.write(ch.prettify())
        
    # Replace in soup
    placeholder = soup.new_string(f"<!-- CHAPTER_{i:02d}_PLACEHOLDER -->")
    ch.replace_with(placeholder)

with io.open('index_skeleton.html', 'w', encoding='utf-8') as out_f:
    out_f.write(soup.prettify())

print("Split complete. Skeleton saved to index_skeleton.html.")
