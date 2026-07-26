import os
import re
import json
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
chapters_dir = os.path.join(base_dir, "chapters")
output_dir = os.path.join(base_dir, "verification_images")
tasks_file = os.path.join(base_dir, "verification_tasks.json")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_tasks = []
download_tasks = []

def download_image(url, local_path):
    if not url.startswith('http'):
        return False, url
    if os.path.exists(local_path):
        return True, url
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response, open(local_path, 'wb') as out_file:
            out_file.write(response.read())
        return True, url
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False, url

total_images = 0

for i in range(1, 82):
    filename = f"chapter_{i:02d}.html"
    filepath = os.path.join(chapters_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
            
        total_images += 1
        caption_text = "No caption found"
        figure_num = "Unknown"
        
        parent = img.parent
        if parent:
            text = parent.get_text(separator=" ", strip=True)
            if re.search(r'Fig(?:ure)?\s*\d+', text, re.IGNORECASE):
                caption_text = text
            else:
                next_sibling = parent.find_next_sibling()
                if next_sibling:
                    text_next = next_sibling.get_text(separator=" ", strip=True)
                    if re.search(r'Fig(?:ure)?\s*\d+', text_next, re.IGNORECASE):
                        caption_text = text_next
        
        fig_match = re.search(r'(Fig(?:ure)?\.?\s*\d+(?:\.\d+)?)', caption_text, re.IGNORECASE)
        if fig_match:
            figure_num = fig_match.group(1)
            
        local_filename = f"ch{i:02d}_fig_{total_images}.jpg"
        local_path = os.path.join(output_dir, local_filename)
        
        download_tasks.append((src, local_path))
        
        all_tasks.append({
            "chapter": i,
            "figure_num": figure_num,
            "image_path": local_path,
            "caption": caption_text
        })

print(f"Starting download of {len(download_tasks)} images in parallel...")

success_count = 0
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(download_image, src, path): src for src, path in download_tasks}
    for future in as_completed(futures):
        success, url = future.result()
        if success:
            success_count += 1

with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(all_tasks, f, indent=2)

print(f"Successfully downloaded {success_count} images. Created tasks file.")
