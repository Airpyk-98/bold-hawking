with open('chapters/chapter_09.html', 'r', encoding='utf-8') as f:
    ch9 = f.read()

# Fix Hamill et al. (2000) DOI
ch9 = ch9.replace('10.1016/S0378-8741(99)00230-7', '10.1016/s0378-8741(00)00180-x')

# Fix Turker & Camper (2002) DOI
ch9 = ch9.replace('10.1016/S0378-8741(02)00159-3', '10.1016/s0378-8741(02)00186-1')

# Remove Zahradnik broken DOI
ch9 = ch9.replace(' <a href="https://doi.org/10.1201/9780429243730-18">https://doi.org/10.1201/9780429243730-18</a>', '')

# Remove Zheleva-Dimitrova broken DOI
ch9 = ch9.replace(' <a href="https://doi.org/10.4103/0973-1296.113294">https://doi.org/10.4103/0973-1296.113294</a>', '')

with open('chapters/chapter_09.html', 'w', encoding='utf-8') as f:
    f.write(ch9)

print("Chapter 9 DOIs updated!")
