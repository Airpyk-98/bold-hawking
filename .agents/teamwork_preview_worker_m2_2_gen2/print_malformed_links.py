import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

chapters = [f'chapters/chapter_{i:02d}.html' for i in range(8, 15)]

for filepath in chapters:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        if '&lt;a' in line or 'splitrock' in line or 'researchgate' in line:
            print(f"{filepath}:{idx+1}: {line.strip()}")
