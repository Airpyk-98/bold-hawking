import os
import sys
import re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def clean_nested_anchors(html):
    # Regex to flatten double nested anchor tags
    pattern = r'<a\s+href=["\']([^"\']+)["\']\s*>\s*<a\s+href=["\']([^"\']+)["\']\s*>(.*?)</a>\s*</a>'
    def repl(m):
        href1, href2, inner = m.group(1), m.group(2), m.group(3)
        return f'<a href="{href1}">{inner}</a>'
    # Run twice for any deeply nested tags
    html = re.sub(pattern, repl, html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(pattern, repl, html, flags=re.DOTALL | re.IGNORECASE)
    return html

def fix_splitrock_links(html):
    # Clean up any broken Splitrock hrefs across all files
    # 1. chapter 8
    html = html.replace(
        '<a href="&lt;a href=" https:="" splitrockenvironmental.ca"=""><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/products/common-juniper-tsiktsektaz?variant=40347042218150"&gt;',
        '<a href="https://splitrockenvironmental.ca/products/common-juniper-tsiktsektaz?variant=40347042218150">https://splitrockenvironmental.ca/products/common-juniper-tsiktsektaz?variant=40347042218150</a>'
    )
    html = html.replace(
        '<a href="https://splitrockenvironmental.ca"><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/products/common-juniper-tsiktsektaz?variant=40347042218150',
        '<a href="https://splitrockenvironmental.ca/products/common-juniper-tsiktsektaz?variant=40347042218150">https://splitrockenvironmental.ca/products/common-juniper-tsiktsektaz?variant=40347042218150</a>'
    )
    
    # 2. chapter 10
    html = html.replace(
        '<a href="https://splitrockenvironmental.ca"><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/products/prairie-rose-qel-q?variant=40368083304614',
        '<a href="https://splitrockenvironmental.ca/products/prairie-rose-qel-q?variant=40368083304614">https://splitrockenvironmental.ca/products/prairie-rose-qel-q?variant=40368083304614</a>'
    )

    # 3. chapter 11
    html = html.replace(
        '<a href="&lt;a href=" https:="" splitrockenvironmental.ca"="">https://splitrockenvironmental.ca</a>/products/big-sagebrush-"&gt;\n<a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a>/products/big-sagebrush-',
        '<a href="https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294">https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294</a>'
    )
    html = html.replace(
        '<a href="&lt;a href=" https:="" splitrockenvironmental.ca"="">https://splitrockenvironmental.ca</a>/products/big-sagebrush-kawkwu?variant=40347062960294"&gt;\n<a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a>/products/big-sagebrush-kawkwu?variant=40347062960294',
        '<a href="https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294">https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294</a>'
    )

    # 4. chapter 12
    html = html.replace(
        '<a href="&lt;a href=" https:="" splitrockenvironmental.ca"=""><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/products/stinging-nettle-salve?variant=33785190744123"&gt;',
        '<a href="https://splitrockenvironmental.ca/products/stinging-nettle-salve?variant=33785190744123">https://splitrockenvironmental.ca/products/stinging-nettle-salve?variant=33785190744123</a>'
    )
    html = html.replace(
        '<a href="https://splitrockenvironmental.ca"><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/products/stinging-nettle-salve?variant=33785190744123',
        '<a href="https://splitrockenvironmental.ca/products/stinging-nettle-salve?variant=33785190744123">https://splitrockenvironmental.ca/products/stinging-nettle-salve?variant=33785190744123</a>'
    )

    # 5. chapter 13
    html = html.replace(
        '<a href="&lt;a href=" https:="" splitrockenvironmental.ca"=""><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518"&gt;',
        '<a href="https://splitrockenvironmental.ca/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518">https://splitrockenvironmental.ca/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518</a>'
    )
    html = html.replace(
        '<a href="https://splitrockenvironmental.ca"><a href="https://splitrockenvironmental.ca">https://splitrockenvironmental.ca</a></a>/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518',
        '<a href="https://splitrockenvironmental.ca/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518">https://splitrockenvironmental.ca/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518</a>'
    )
    return html

def fix_researchgate_links(html):
    # Fix split researchgate figure links in chapter 12
    html = re.sub(
        r'<a\s+href="https://www\.researchgate\.net/figure/Some-important-amino-based-neurotransmitters_fig1_353203150">\s*https://www\.researchgate\.net/figure/Some-important-amino-based-\s*</a>\s*<a\s+href="https://www\.researchgate\.net/figure/Some-important-amino-based-neurotransmitters_fig1_353203150">\s*neurotransmitters_fig1_353203150\s*</a>',
        r'<a href="https://www.researchgate.net/figure/Some-important-amino-based-neurotransmitters_fig1_353203150">https://www.researchgate.net/figure/Some-important-amino-based-neurotransmitters_fig1_353203150</a>',
        html, flags=re.IGNORECASE | re.DOTALL
    )
    html = re.sub(
        r'<a\s+href="https://www\.researchgate\.net/figure/Molecular-structure-of-chlorophyll-a-and-chlorophyll-b_fig1_283281046">\s*https://www\.researchgate\.net/figure/Molecular-structure-of-chlorophyll-a-and-\s*</a>\s*<a\s+href="https://www\.researchgate\.net/figure/Molecular-structure-of-chlorophyll-a-and-chlorophyll-b_fig1_283281046">\s*chlorophyll-b_fig1_283281046\s*</a>',
        r'<a href="https://www.researchgate.net/figure/Molecular-structure-of-chlorophyll-a-and-chlorophyll-b_fig1_283281046">https://www.researchgate.net/figure/Molecular-structure-of-chlorophyll-a-and-chlorophyll-b_fig1_283281046</a>',
        html, flags=re.IGNORECASE | re.DOTALL
    )
    return html

# Perform fixes chapter by chapter
print("Applying HTML and Reference fixes to Chapters 8 through 14...")

# ==========================================
# CHAPTER 8
# ==========================================
with open('chapters/chapter_08.html', 'r', encoding='utf-8') as f:
    ch8_html = f.read()

ch8_html = clean_nested_anchors(ch8_html)
ch8_html = fix_splitrock_links(ch8_html)

with open('chapters/chapter_08.html', 'w', encoding='utf-8') as f:
    f.write(ch8_html)
print("Chapter 8 updated successfully!")


# ==========================================
# CHAPTER 9
# ==========================================
with open('chapters/chapter_09.html', 'r', encoding='utf-8') as f:
    ch9_html = f.read()

ch9_ol_content = """<ol>
<li>1. Akdemir, Z. S., Tatli, I. I., Saracoglu, I., &amp; Ismailoglu, U. B. (2001). Polyphenolic compounds from <em>Verbascum lasianthum</em> and <em>Verbascum urticaefolium</em>. <em>Turkish Journal of Chemistry</em>, <em>25</em>(4), 415–420.</li>
<li>2. Alipieva, K., Korkina, L., Orhan, I. E., &amp; Georgiev, M. I. (2014). Verbascoside—A review of its occurrence, (bio)synthesis and pharmacological significance. <em>Biotechnology Advances</em>, <em>32</em>(6), 1065–1076. <a href="https://doi.org/10.1016/j.biotechadv.2014.07.001">https://doi.org/10.1016/j.biotechadv.2014.07.001</a></li>
<li>3. Dulger, B., &amp; Gonuz, A. (2004). Antimicrobial activity of some Turkish medicinal plants. <em>Pakistan Journal of Biological Sciences</em>, <em>7</em>(9), 1559–1562. <a href="https://doi.org/10.3923/pjbs.2004.1559.1562">https://doi.org/10.3923/pjbs.2004.1559.1562</a></li>
<li>4. Elders and Community Members of the Cayoose Creek Band of Sekw’el’was. (n.d.). Personal communication.</li>
<li>5. Hamill, F. A., Apio, S., Mubiru, N. K., Mosango, M., Bukenya-Ziraba, R., Maganyi, O. W., &amp; Soejarto, D. D. (2000). Traditional herbal drugs of southern Uganda, I. <em>Journal of Ethnopharmacology</em>, <em>70</em>(3), 281–300. <a href="https://doi.org/10.1016/S0378-8741(99)00230-7">https://doi.org/10.1016/S0378-8741(99)00230-7</a></li>
<li>6. Jones, A. (2024). <em>Medicinal herbs of western Canada</em> (1st ed.). Nimbus Publishing.</li>
<li>7. Kupeli, E., Kosar, M., Yesilada, E., Hüsnu Can Baser, K., &amp; Başer, C. (2005). A comparative study on the anti-inflammatory, antinociceptive and antipyretic effects of isoquinoline alkaloids from the roots of Turkish Berberis species. <em>Life Sciences</em>, <em>72</em>(6), 645–657. <a href="https://doi.org/10.1016/j.lfs.2003.09.053">https://doi.org/10.1016/j.lfs.2003.09.053</a></li>
<li>8. McCutcheon, A. R., Roberts, T. E., Gibbons, E., Ellis, S. M., Babiuk, L. A., Hancock, R. E., &amp; Towers, G. H. N. (1995). Antiviral screening of British Columbian medicinal plants. <em>Journal of Ethnopharmacology</em>, <em>49</em>(2), 101–110. <a href="https://doi.org/10.1016/0378-8741(95)01321-0">https://doi.org/10.1016/0378-8741(95)01321-0</a></li>
<li>9. Moerman, D. E. (1998). <em>Native American ethnobotany</em>. Timber Press.</li>
<li>10. Riaz, M., Zia-Ul-Haq, M., &amp; Jaafar, H. Z. E. (2013). Common mullein, pharmacological and chemical aspects. <em>Revista Brasileira de Farmacognosia</em>, <em>23</em>(6), 948–959. <a href="https://doi.org/10.1590/S0102-695X2013000600004">https://doi.org/10.1590/S0102-695X2013000600004</a></li>
<li>11. Sarić-Kundalić, B., Dobeš, C., Klatte-Asselmeyer, V., &amp; Saukel, J. (2010). Ethnobotanical study on medicinal use of wild and cultivated plants in middle, south and west Bosnia and Herzegovina. <em>Journal of Ethnopharmacology</em>, <em>131</em>(1), 33–55. <a href="https://doi.org/10.1016/j.jep.2010.05.061">https://doi.org/10.1016/j.jep.2010.05.061</a></li>
<li>12. Sarrell, E. M., Mandelberg, A., &amp; Cohen, H. A. (2001). Efficacy of naturopathic extracts in the management of ear pain associated with acute otitis media. <em>Archives of Pediatrics &amp; Adolescent Medicine</em>, <em>155</em>(7), 796–799. <a href="https://doi.org/10.1001/archpedi.155.7.796">https://doi.org/10.1001/archpedi.155.7.796</a></li>
<li>13. Tatli, I. I., &amp; Akdemir, Z. S. (2004). Traditional uses and biological activities of Verbascum species. <em>FABAD Journal of Pharmaceutical Sciences</em>, <em>29</em>, 85–96.</li>
<li>14. Tatli, I. I., Akdemir, Z., Yesilada, E., &amp; Küpeli, E. (2004). Anti-inflammatory and antinociceptive potential of major phenolics from <em>Verbascum salviifolium</em>. <em>Zeitschrift für Naturforschung C</em>, <em>59</em>(5–6), 609–613. <a href="https://doi.org/10.1515/znc-2004-5-622">https://doi.org/10.1515/znc-2004-5-622</a></li>
<li>15. Turker, A. U., &amp; Camper, N. D. (2002). Biological activity of common mullein, a medicinal plant. <em>Journal of Ethnopharmacology</em>, <em>82</em>(2–3), 117–125. <a href="https://doi.org/10.1016/S0378-8741(02)00159-3">https://doi.org/10.1016/S0378-8741(02)00159-3</a></li>
<li>16. Zahradnik, H. P., &amp; Goldmeier, S. (2020). Phytotherapy for dysmenorrhea, endometriosis, and premenstrual syndrome. In I. E. Orhan (Ed.), <em>Herbal medicine</em> (pp. 323–342). CRC Press. <a href="https://doi.org/10.1201/9780429243730-18">https://doi.org/10.1201/9780429243730-18</a></li>
<li>17. Zgorniak-Nowosielska, I., Grzybek, J., Manolova, N., Serkedjieva, J., &amp; Zawilinska, B. (1991). Antiviral activity of Flos Verbasci infusion against Influenza and Herpes simplex viruses. <em>Archivum Immunologiae et Therapiae Experimentalis</em>, <em>39</em>, 103–108.</li>
<li>18. Zheleva-Dimitrova, D., Obreshkova, D., &amp; Nedialkov, P. (2013). Antioxidant activity of iridoid glucosides from <em>Veronica chamaedrys</em>. <em>Pharmacognosy Magazine</em>, <em>9</em>(35), 268–273. <a href="https://doi.org/10.4103/0973-1296.113294">https://doi.org/10.4103/0973-1296.113294</a></li>
</ol>"""

# Strip leading numbers in <li> items for clean <ol>
ch9_ol_clean = re.sub(r'<li>\d+\.\s*', '<li>', ch9_ol_content)

# Insert after References heading if missing
ref_p = '<p><span style="color: #339966"><strong>References</strong></span></p>'
if ref_p in ch9_html:
    ch9_html = ch9_html.replace(ref_p, ref_p + '\n' + ch9_ol_clean)
elif 'References' in ch9_html:
    ch9_html = re.sub(r'(<p>[^<]*References[^<]*</p>)', r'\1\n' + ch9_ol_clean, ch9_html, flags=re.IGNORECASE)

with open('chapters/chapter_09.html', 'w', encoding='utf-8') as f:
    f.write(ch9_html)
print("Chapter 9 reference section restored & updated successfully!")


# ==========================================
# CHAPTER 10
# ==========================================
with open('chapters/chapter_10.html', 'r', encoding='utf-8') as f:
    ch10_html = f.read()

ch10_html = clean_nested_anchors(ch10_html)
ch10_html = fix_splitrock_links(ch10_html)

with open('chapters/chapter_10.html', 'w', encoding='utf-8') as f:
    f.write(ch10_html)
print("Chapter 10 updated successfully!")


# ==========================================
# CHAPTER 11
# ==========================================
with open('chapters/chapter_11.html', 'r', encoding='utf-8') as f:
    ch11_html = f.read()

ch11_html = fix_splitrock_links(ch11_html)

# Fix specific DOIs in chapter 11:
# Item 1: Replace 10.1093/ecam/neh050 with 10.1093/ecam/neh072
ch11_html = ch11_html.replace('10.1093/ecam/neh050', '10.1093/ecam/neh072')

# Item 12: Replace 10.1007/s40268-016-0157-8 with 10.1007/s40268-016-0157-5
ch11_html = ch11_html.replace('10.1007/s40268-016-0157-8', '10.1007/s40268-016-0157-5')

# Item 17: Replace 10.1021/jf100871b with 10.1021/jf100082p
ch11_html = ch11_html.replace('10.1021/jf100871b', '10.1021/jf100082p')

# Item 19: Remove hallucinated 10.1159/000346229
ch11_html = ch11_html.replace('<a href="https://doi.org/10.1159/000346229">https://doi.org/10.1159/000346229</a>', '')
ch11_html = ch11_html.replace('https://doi.org/10.1159/000346229', '')

# Item 22: Replace 10.1007/BF02860478 with 10.1007/BF02860489
ch11_html = ch11_html.replace('10.1007/BF02860478', '10.1007/BF02860489')

# Now convert the 23 <p> reference items into an <ol> list
soup = BeautifulSoup(ch11_html, 'html.parser')
p_tags = soup.find_all('p')
ref_p_tags = [p for p in p_tags if re.match(r'^\s*\d+\.\s+', p.get_text())]

if ref_p_tags:
    ol_tag = soup.new_tag('ol')
    for p in ref_p_tags:
        li = soup.new_tag('li')
        # Copy inner HTML of paragraph
        li.extend(p.contents)
        # Strip leading "1. ", "2. ", etc. from the first text node of <li>
        if li.contents:
            first_node = li.contents[0]
            if isinstance(first_node, str):
                cleaned_text = re.sub(r'^\s*\d+\.\s*', '', first_node)
                first_node.replace_with(cleaned_text)
        ol_tag.append(li)
    
    # Replace the first reference <p> with the new <ol> tag and decompose remaining <p> tags
    ref_p_tags[0].replace_with(ol_tag)
    for p in ref_p_tags[1:]:
        p.decompose()

ch11_html = str(soup)
ch11_html = clean_nested_anchors(ch11_html)

with open('chapters/chapter_11.html', 'w', encoding='utf-8') as f:
    f.write(ch11_html)
print("Chapter 11 <p> list converted to <ol> and updated successfully!")


# ==========================================
# CHAPTER 12
# ==========================================
with open('chapters/chapter_12.html', 'r', encoding='utf-8') as f:
    ch12_html = f.read()

ch12_html = clean_nested_anchors(ch12_html)
ch12_html = fix_splitrock_links(ch12_html)
ch12_html = fix_researchgate_links(ch12_html)

# Item 8: Replace hallucinated 10.1055/s-2000-11120 with true 10.1055/s-2000-11117
ch12_html = ch12_html.replace('10.1055/s-2000-11120', '10.1055/s-2000-11117')

with open('chapters/chapter_12.html', 'w', encoding='utf-8') as f:
    f.write(ch12_html)
print("Chapter 12 updated successfully!")


# ==========================================
# CHAPTER 13
# ==========================================
with open('chapters/chapter_13.html', 'r', encoding='utf-8') as f:
    ch13_html = f.read()

ch13_html = clean_nested_anchors(ch13_html)
ch13_html = fix_splitrock_links(ch13_html)

# Item 1: Add true DOI 10.29228/jrp.607
ch13_html = ch13_html.replace(
    '<a href="https://www.jrespharm.com/uploads/pdf/pdf_MPJ_1485.pdf">https://www.jrespharm.com/uploads/pdf/pdf_MPJ_1485.pdf</a>',
    '<a href="https://www.jrespharm.com/uploads/pdf/pdf_MPJ_1485.pdf">https://www.jrespharm.com/uploads/pdf/pdf_MPJ_1485.pdf</a> <a href="https://doi.org/10.29228/jrp.607">https://doi.org/10.29228/jrp.607</a>'
)

# Item 4: Remove broken DOI 10.5923/j.chemistry.20211102.02
ch13_html = ch13_html.replace('<a href="https://doi.org/10.5923/j.chemistry.20211102.02">https://doi.org/10.5923/j.chemistry.20211102.02</a>', '')
ch13_html = ch13_html.replace('https://doi.org/10.5923/j.chemistry.20211102.02', '')

with open('chapters/chapter_13.html', 'w', encoding='utf-8') as f:
    f.write(ch13_html)
print("Chapter 13 updated successfully!")


# ==========================================
# CHAPTER 14
# ==========================================
with open('chapters/chapter_14.html', 'r', encoding='utf-8') as f:
    ch14_html = f.read()

ch14_html = clean_nested_anchors(ch14_html)

with open('chapters/chapter_14.html', 'w', encoding='utf-8') as f:
    f.write(ch14_html)
print("Chapter 14 updated successfully!")

print("\nALL CHAPTERS 8-14 SUCCESSFULLY UPDATED AND CLEANED!")
