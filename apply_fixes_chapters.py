import re
import os

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
chapters_dir = os.path.join(base_dir, "chapters")
errors_file = r"C:\Users\DELL\.gemini\antigravity\brain\6a70ced1-308c-4b55-8f91-d40f1d746322\caption_errors.md"

with open(errors_file, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

# Parse fixes and which chapter they belong to
fixes = []
current_chapter = None
current_fig = None

for line in lines:
    line = line.strip()
    match = re.search(r'\*\*(?:Chapter (\d+),\s*)?(Fig(?:ure)? \d+\.\d+)\*\*', line, re.IGNORECASE)
    if match:
        current_chapter = int(match.group(1)) if match.group(1) else None
        current_fig = match.group(2).replace('Figure', 'Fig')
    else:
        cap_match = re.match(r'^-\s*\*\*Correct.*?\*\*\s*:?\s*(.*)', line, re.IGNORECASE)
        if cap_match and current_fig and current_chapter:
            val = cap_match.group(1).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            fixes.append({'chapter': current_chapter, 'fig': current_fig, 'correct_text': val})
            current_fig = None

print(f"Loaded {len(fixes)} targeted fixes.")

applied = 0
for fix in fixes:
    chap_num = fix['chapter']
    fig = fix['fig']
    correct_text = fix['correct_text']
    
    chap_file = os.path.join(chapters_dir, f"chapter_{chap_num:02d}.html")
    if not os.path.exists(chap_file):
        print(f"File {chap_file} does not exist.")
        continue
        
    with open(chap_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    clean_correct = correct_text
    prefix_match = re.match(r'^(?:Fig(?:ure)?\s*\d+\.\d+[:\-\s]+)(.*)', correct_text, re.IGNORECASE)
    if prefix_match:
        clean_correct = prefix_match.group(1).strip()
        
    escaped_fig = fig.replace('.', r'\.')
    pattern = r'(' + escaped_fig + r'[:\-\s]+)(.*?)(?=</strong|</b|</p|</figcaption|<br)'
    
    def replacer(m):
        prefix = m.group(1)
        return prefix + clean_correct

    new_content, count = re.subn(pattern, replacer, content, count=1, flags=re.IGNORECASE|re.DOTALL)
    if count > 0:
        with open(chap_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[SUCCESS] Edited {fig} in chapter_{chap_num:02d}.html")
        applied += 1
    else:
        print(f"[FAIL] Could not find {fig} in chapter_{chap_num:02d}.html")

print(f"Completed targeted edits. Applied {applied} out of {len(fixes)}.")
