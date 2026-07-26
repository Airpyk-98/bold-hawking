import os
import re
from bs4 import BeautifulSoup

chapters_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

def fix_chapter(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    imgs = soup.find_all('img')
    if not imgs:
        return False

    # Find text nodes starting with "Fig X.Y:"
    # This prevents matching outer wrapper tags multiple times.
    new_captions = []
    pattern = re.compile(r'^\s*Fig \d+\.\d+:')
    for text_node in soup.find_all(string=pattern):
        # The parent is the innermost tag containing the text
        inner_tag = text_node.parent
        container = inner_tag.find_parent('p')
        target = container if container else inner_tag
        if target not in new_captions:
            # Check if this target is an ancestor of an existing target, or vice versa
            # to be absolutely sure we don't duplicate.
            is_duplicate = False
            for existing in new_captions:
                if target in existing.parents or existing in target.parents:
                    is_duplicate = True
                    break
            if not is_duplicate:
                new_captions.append(target)

    if len(imgs) == len(new_captions):
        pairs = list(zip(imgs, new_captions))
        for img, caption in pairs:
            # We must be careful: if img is inside the caption container, extract it first before doing anything!
            # Wait, if img is INSIDE the caption container (e.g. they share the same outer <p>)
            # Yes, they might share the outer <p>.
            # orig_parent is the closest <p> to img. 
            orig_parent = img.find_parent('p')
            
            new_img_p = soup.new_tag('p', style='text-align: center;')
            
            if orig_parent and orig_parent.parent:
                orig_parent.insert_before(new_img_p)
            elif img.parent:
                img.insert_before(new_img_p)
                
            extracted_img = img.extract()
            new_img_p.append(extracted_img)
            
            extracted_caption = caption.extract()
            new_img_p.insert_after(extracted_caption)
    else:
        print(f"Warning: {os.path.basename(filename)} - img count ({len(imgs)}) != caption count ({len(new_captions)})")

    # Final cleanup pass for legacy captions and empty tags
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        # Match legacy captions e.g. "Figure 1:", "Fig 1:", "Figure 1.1:"
        if re.match(r'^(Figure|Fig\.?)\s*\d+[\.:\-\s]', text, re.IGNORECASE) and not re.match(r'^Fig \d+\.\d+:', text):
            if len(text) < 250:
                p.extract()
        # Delete empty paragraphs left behind
        elif not text and not p.find('img'):
            p.extract()

    # Some legacy captions might be inside div or just standalone strong tags.
    for strong in soup.find_all(['strong', 'b', 'span']):
        text = strong.get_text(strip=True)
        if re.match(r'^(Figure|Fig\.?)\s*\d+[\.:\-\s]', text, re.IGNORECASE) and not re.match(r'^Fig \d+\.\d+:', text):
            parent = strong.parent
            if parent and parent.name == 'p':
                parent_text = parent.get_text(strip=True)
                if len(parent_text) < 250:
                    parent.extract()
            else:
                strong.extract()

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    return True

processed = 0
for i in range(1, 82):
    filename = os.path.join(chapters_dir, f"chapter_{i:02d}.html")
    if os.path.exists(filename):
        if fix_chapter(filename):
            processed += 1

print(f"Done fixing captions in {processed} chapters.")
