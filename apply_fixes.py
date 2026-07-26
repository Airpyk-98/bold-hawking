import os
import re
from bs4 import BeautifulSoup

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
chapters_dir = os.path.join(base_dir, "chapters")
errors_file = r"C:\Users\DELL\.gemini\antigravity\brain\6a70ced1-308c-4b55-8f91-d40f1d746322\caption_errors.md"

with open(errors_file, 'r', encoding='utf-8') as f:
    content = f.read()

corrections = []
lines = content.split('\n')
current_fig = None

for i, line in enumerate(lines):
    # Just look for any mention of "Fig X.Y" or "Figure X.Y" on lines that look like headings or bullets
    if re.search(r'(?:\*\*|#|- |\d+\.\s)', line):
        fig_match = re.search(r'Fig(?:ure)?\s*(\d+\.\d+)', line, re.IGNORECASE)
        if fig_match:
            current_fig = fig_match.group(1)
            
    if 'Correct Caption:' in line or 'Correct Description:' in line or 'Corrected Caption:' in line:
        if current_fig:
            correct_text = re.split(r'Correct(?:ed)? (?:Caption|Description):\**\s*', line, flags=re.IGNORECASE)[1].strip()
            correct_text = re.sub(r'\s*\(\*?Note:.*', '', correct_text, flags=re.IGNORECASE)
            correct_text = correct_text.strip('_* ')
            
            if not correct_text.startswith(f'Fig {current_fig}') and not correct_text.startswith(f'Figure {current_fig}'):
                correct_text = f"Fig {current_fig}: {correct_text}"
                
            chapter = int(current_fig.split('.')[0])
            corrections.append({
                'chapter': chapter,
                'fig': current_fig,
                'text': correct_text
            })
            current_fig = None

print(f"Found {len(corrections)} corrections to apply.")
for c in corrections:
    print(f"Ch {c['chapter']} {c['fig']} -> {c['text'][:50]}...")

applied_count = 0
for c in corrections:
    chapter = c['chapter']
    fig = c['fig']
    new_text = c['text']
    
    filename = f"chapter_{chapter:02d}.html"
    filepath = os.path.join(chapters_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"File {filepath} not found!")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    found = False
    escaped_fig = fig.replace('.', r'\.')
    
    # Try to find the exact text in elements
    for el in soup.find_all(string=re.compile(f'Fig(?:ure)?\.?\\s*{escaped_fig}', re.IGNORECASE)):
        parent = el.parent
        if parent and parent.name in ['p', 'div', 'span', 'figcaption', 'strong', 'em', 'b', 'i']:
            el.replace_with(new_text)
            found = True
            applied_count += 1
            break
            
    if not found:
        print(f"Could not find caption for {fig} in {filename}")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))

print(f"Successfully applied {applied_count} corrections.")
