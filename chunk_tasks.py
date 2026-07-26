import json
import os

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
tasks_file = os.path.join(base_dir, "verification_tasks.json")
chunks_file = os.path.join(base_dir, "task_chunks.json")

# Wait for tasks_file to exist
import time
while not os.path.exists(tasks_file):
    time.sleep(1)

with open(tasks_file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

# Group tasks by chapter
from collections import defaultdict
tasks_by_chapter = defaultdict(list)
for t in tasks:
    tasks_by_chapter[t['chapter']].append(t)

chunks = []
current_chunk = []
current_chapters = set()

for chapter in sorted(tasks_by_chapter.keys()):
    current_chunk.extend(tasks_by_chapter[chapter])
    current_chapters.add(chapter)
    
    if len(current_chapters) >= 5:
        chunks.append({
            "chapters": f"{min(current_chapters)}-{max(current_chapters)}",
            "tasks": current_chunk
        })
        current_chunk = []
        current_chapters = set()

if current_chunk:
    chunks.append({
        "chapters": f"{min(current_chapters)}-{max(current_chapters)}",
        "tasks": current_chunk
    })

with open(chunks_file, 'w', encoding='utf-8') as f:
    json.dump(chunks, f, indent=2)

print(f"Created {len(chunks)} chunks.")
