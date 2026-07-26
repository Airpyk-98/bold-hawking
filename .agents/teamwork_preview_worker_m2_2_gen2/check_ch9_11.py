import re

with open('chapters/chapter_09.html', 'r', encoding='utf-8') as f:
    ch9 = f.read()

print('=== Chapter 9 References check ===')
if '<ol>' in ch9:
    print('OL present in chapter 9!')
    print('DOIs in ch9:', len(re.findall(r'doi\.org', ch9)))
    # Print the references section
    idx = ch9.find('References')
    if idx != -1:
        print('Snippet:', ch9[idx:idx+1500])
else:
    print('OL NOT PRESENT in chapter 9!')

with open('chapters/chapter_11.html', 'r', encoding='utf-8') as f:
    ch11 = f.read()

print('=== Chapter 11 Bad Href check ===')
bad_hrefs = re.findall(r'<a\s+[^>]*href=["\']&lt;a\s+href=.*?', ch11, re.IGNORECASE)
print('Bad hrefs in ch11:', len(bad_hrefs))
for b in bad_hrefs:
    print('  ', repr(b[:120]))
