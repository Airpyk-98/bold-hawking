with open('chapters/chapter_09.html', 'r', encoding='utf-8') as f:
    ch9 = f.read()

print("CH 9 References snippet:")
idx = ch9.lower().find('references')
if idx != -1:
    print(repr(ch9[idx-50:idx+300]))

with open('chapters/chapter_11.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\nCH 11 bad href lines:")
for i, l in enumerate(lines):
    if '&lt;a' in l or 'splitrock' in l:
        print(f"Line {i+1}: {repr(l)}")
