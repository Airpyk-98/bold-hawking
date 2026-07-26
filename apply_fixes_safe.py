import re
import os

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
errors_file = r"C:\Users\DELL\.gemini\antigravity\brain\6a70ced1-308c-4b55-8f91-d40f1d746322\caption_errors.md"
input_html = os.path.join(base_dir, "vercel_deploy", "index.html")
output_html = os.path.join(base_dir, "index_corrected.html")

with open(errors_file, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

fixes = {}
current_fig = None
for line in lines:
    line = line.strip()
    match = re.search(r'\*\*(?:Chapter \d+,\s*)?(Fig(?:ure)? \d+\.\d+)\*\*', line, re.IGNORECASE)
    if match:
        current_fig = match.group(1).replace('Figure', 'Fig')
    else:
        cap_match = re.match(r'^-\s*\*\*Correct.*?\*\*\s*:?\s*(.*)', line, re.IGNORECASE)
        if cap_match and current_fig:
            val = cap_match.group(1).strip()
            # strip surrounding quotes if present
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            fixes[current_fig] = val
            current_fig = None

with open(input_html, 'r', encoding='utf-8') as f:
    content = f.read()

applied_count = 0
for fig, correct_text in fixes.items():
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
        applied_count += 1
        content = new_content
    else:
        print(f"Failed to find {fig} in HTML.")

print(f"Successfully applied {applied_count} fixes out of {len(fixes)}.")

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(content)
