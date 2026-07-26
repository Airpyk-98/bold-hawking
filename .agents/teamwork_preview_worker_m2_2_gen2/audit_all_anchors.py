import os
import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

chapters = [f'chapters/chapter_{i:02d}.html' for i in range(8, 15)]

for filepath in chapters:
    print('========================================')
    print('AUDITING ANCHORS IN:', filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find any &lt;a href= or malformed hrefs
    malformed_hrefs = re.findall(r'<a\s+[^>]*&lt;a\s+[^>]*>', html, re.IGNORECASE)
    print(f"Malformed &lt;a> count: {len(malformed_hrefs)}")

    # Find nested <a> tags
    nested_a = re.findall(r'<a\s+[^>]*>\s*<a\s+[^>]*>.*?</a>\s*</a>', html, re.DOTALL | re.IGNORECASE)
    print(f"Nested <a> count: {len(nested_a)}")
    for n in nested_a[:3]:
        print("   Sample nested:", repr(n[:150]))

    # Find any anchor with href containing &lt; or quotes inside quotes
    bad_attrs = re.findall(r'<a\s+[^>]*href=["\'][^"\']*&lt;[^"\']*["\'][^>]*>', html, re.IGNORECASE)
    print(f"Bad href attr count: {len(bad_attrs)}")
    for b in bad_attrs[:3]:
        print("   Sample bad attr:", repr(b[:150]))

    # Find any ResearchGate or split <a> tags
    rg_tags = re.findall(r'<a\s+[^>]*researchgate[^>]*>', html, re.IGNORECASE)
    print(f"ResearchGate tags count: {len(rg_tags)}")
