import os
import re
from bs4 import BeautifulSoup

chapters_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
chapter_files = [f"chapter_{str(i).zfill(2)}.html" for i in range(8, 15)]

out_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_2\ref_structure_report.txt"

with open(out_path, "w", encoding="utf-8") as out:
    for ch_file in chapter_files:
        path = os.path.join(chapters_dir, ch_file)
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        out.write(f"\n==========================================\n")
        out.write(f"FILE: {ch_file}\n")
        out.write(f"==========================================\n")
        
        ref_nodes = soup.find_all(string=re.compile(r'References', re.IGNORECASE))
        out.write(f"Found {len(ref_nodes)} nodes containing 'References':\n")
        for r in ref_nodes:
            parent = r.parent
            grandparent = parent.parent if parent else None
            gp_tag = grandparent.name if grandparent else None
            out.write(f"  Node: '{r.strip()}' | Parent tag: <{parent.name}> | Grandparent: <{gp_tag}>\n")
            
            # Check what comes after this parent/grandparent
            block = parent
            while block and block.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']:
                block = block.parent
                
            next_ol = block.find_next("ol") if block else None
            if next_ol:
                li_count = len(next_ol.find_all("li", recursive=False))
                first_li = next_ol.find("li").get_text(strip=True)[:80] if next_ol.find("li") else "Empty"
                out.write(f"  -> Following <ol>: li_count={li_count}, First li='{first_li}'\n")
            else:
                out.write(f"  -> NO FOLLOWING <ol> FOUND!\n")
                
        ols = soup.find_all('ol')
        out.write(f"Total <ol> tags in document: {len(ols)}\n")

print("Done writing ref_structure_report.txt")
