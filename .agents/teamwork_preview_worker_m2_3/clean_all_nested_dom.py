import os
from bs4 import BeautifulSoup

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

for ch in range(15, 21):
    fname = f"chapter_{ch}.html"
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    ols = soup.find_all("ol")
    if not ols:
        continue
    ol = ols[-1]
    
    # Loop until no nested <a> tags remain
    changed = True
    while changed:
        changed = False
        for a in ol.find_all("a"):
            child_a = a.find("a")
            if child_a:
                # Replace outer <a> with child_a
                a.replace_with(child_a)
                changed = True
                break
                
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(str(soup))

print("Completed DOM-level nested anchor tag cleanup across Chapters 15-20.")
