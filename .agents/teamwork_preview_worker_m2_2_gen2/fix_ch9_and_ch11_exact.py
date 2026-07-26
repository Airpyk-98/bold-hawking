import re

# 1. Fix Chapter 09
with open('chapters/chapter_09.html', 'r', encoding='utf-8') as f:
    ch9_html = f.read()

ch9_ol_content = """<ol>
<li>Akdemir, Z. S., Tatli, I. I., Saracoglu, I., &amp; Ismailoglu, U. B. (2001). Polyphenolic compounds from <em>Verbascum lasianthum</em> and <em>Verbascum urticaefolium</em>. <em>Turkish Journal of Chemistry</em>, <em>25</em>(4), 415–420.</li>
<li>Alipieva, K., Korkina, L., Orhan, I. E., &amp; Georgiev, M. I. (2014). Verbascoside—A review of its occurrence, (bio)synthesis and pharmacological significance. <em>Biotechnology Advances</em>, <em>32</em>(6), 1065–1076. <a href="https://doi.org/10.1016/j.biotechadv.2014.07.001">https://doi.org/10.1016/j.biotechadv.2014.07.001</a></li>
<li>Dulger, B., &amp; Gonuz, A. (2004). Antimicrobial activity of some Turkish medicinal plants. <em>Pakistan Journal of Biological Sciences</em>, <em>7</em>(9), 1559–1562. <a href="https://doi.org/10.3923/pjbs.2004.1559.1562">https://doi.org/10.3923/pjbs.2004.1559.1562</a></li>
<li>Elders and Community Members of the Cayoose Creek Band of Sekw’el’was. (n.d.). Personal communication.</li>
<li>Hamill, F. A., Apio, S., Mubiru, N. K., Mosango, M., Bukenya-Ziraba, R., Maganyi, O. W., &amp; Soejarto, D. D. (2000). Traditional herbal drugs of southern Uganda, I. <em>Journal of Ethnopharmacology</em>, <em>70</em>(3), 281–300. <a href="https://doi.org/10.1016/S0378-8741(99)00230-7">https://doi.org/10.1016/S0378-8741(99)00230-7</a></li>
<li>Jones, A. (2024). <em>Medicinal herbs of western Canada</em> (1st ed.). Nimbus Publishing.</li>
<li>Kupeli, E., Kosar, M., Yesilada, E., Hüsnu Can Baser, K., &amp; Başer, C. (2005). A comparative study on the anti-inflammatory, antinociceptive and antipyretic effects of isoquinoline alkaloids from the roots of Turkish Berberis species. <em>Life Sciences</em>, <em>72</em>(6), 645–657. <a href="https://doi.org/10.1016/j.lfs.2003.09.053">https://doi.org/10.1016/j.lfs.2003.09.053</a></li>
<li>McCutcheon, A. R., Roberts, T E., Gibbons, E., Ellis, S. M., Babiuk, L. A., Hancock, R. E., &amp; Towers, G. H. N. (1995). Antiviral screening of British Columbian medicinal plants. <em>Journal of Ethnopharmacology</em>, <em>49</em>(2), 101–110. <a href="https://doi.org/10.1016/0378-8741(95)01321-0">https://doi.org/10.1016/0378-8741(95)01321-0</a></li>
<li>Moerman, D. E. (1998). <em>Native American ethnobotany</em>. Timber Press.</li>
<li>Riaz, M., Zia-Ul-Haq, M., &amp; Jaafar, H. Z. E. (2013). Common mullein, pharmacological and chemical aspects. <em>Revista Brasileira de Farmacognosia</em>, <em>23</em>(6), 948–959. <a href="https://doi.org/10.1590/S0102-695X2013000600004">https://doi.org/10.1590/S0102-695X2013000600004</a></li>
<li>Sarić-Kundalić, B., Dobeš, C., Klatte-Asselmeyer, V., &amp; Saukel, J. (2010). Ethnobotanical study on medicinal use of wild and cultivated plants in middle, south and west Bosnia and Herzegovina. <em>Journal of Ethnopharmacology</em>, <em>131</em>(1), 33–55. <a href="https://doi.org/10.1016/j.jep.2010.05.061">https://doi.org/10.1016/j.jep.2010.05.061</a></li>
<li>Sarrell, E. M., Mandelberg, A., &amp; Cohen, H. A. (2001). Efficacy of naturopathic extracts in the management of ear pain associated with acute otitis media. <em>Archives of Pediatrics &amp; Adolescent Medicine</em>, 155(7), 796–799. <a href="https://doi.org/10.1001/archpedi.155.7.796">https://doi.org/10.1001/archpedi.155.7.796</a></li>
<li>Tatli, I. I., &amp; Akdemir, Z. S. (2004). Traditional uses and biological activities of Verbascum species. <em>FABAD Journal of Pharmaceutical Sciences</em>, <em>29</em>, 85–96.</li>
<li>Tatli, I. I., Akdemir, Z., Yesilada, E., &amp; Küpeli, E. (2004). Anti-inflammatory and antinociceptive potential of major phenolics from <em>Verbascum salviifolium</em>. <em>Zeitschrift für Naturforschung C</em>, <em>59</em>(5–6), 609–613. <a href="https://doi.org/10.1515/znc-2004-5-622">https://doi.org/10.1515/znc-2004-5-622</a></li>
<li>Turker, A. U., &amp; Camper, N. D. (2002). Biological activity of common mullein, a medicinal plant. <em>Journal of Ethnopharmacology</em>, <em>82</em>(2–3), 117–125. <a href="https://doi.org/10.1016/S0378-8741(02)00159-3">https://doi.org/10.1016/S0378-8741(02)00159-3</a></li>
<li>Zahradnik, H. P., &amp; Goldmeier, S. (2020). Phytotherapy for dysmenorrhea, endometriosis, and premenstrual syndrome. In I. E. Orhan (Ed.), <em>Herbal medicine</em> (pp. 323–342). CRC Press. <a href="https://doi.org/10.1201/9780429243730-18">https://doi.org/10.1201/9780429243730-18</a></li>
<li>Zgorniak-Nowosielska, I., Grzybek, J., Manolova, N., Serkedjieva, J., &amp; Zawilinska, B. (1991). Antiviral activity of Flos Verbasci infusion against Influenza and Herpes simplex viruses. <em>Archivum Immunologiae et Therapiae Experimentalis</em>, <em>39</em>, 103–108.</li>
<li>Zheleva-Dimitrova, D., Obreshkova, D., &amp; Nedialkov, P. (2013). Antioxidant activity of iridoid glucosides from <em>Veronica chamaedrys</em>. <em>Pharmacognosy Magazine</em>, <em>9</em>(35), 268–273. <a href="https://doi.org/10.4103/0973-1296.113294">https://doi.org/10.4103/0973-1296.113294</a></li>
</ol>"""

# Target exact header string in ch9_html
header_pattern = r'(<p>\s*<span style="color: #339966">\s*<strong>\s*References\s*</strong>\s*</span>\s*</p>)'
if re.search(header_pattern, ch9_html, re.IGNORECASE):
    ch9_html = re.sub(header_pattern, r'\1\n' + ch9_ol_content, ch9_html, flags=re.IGNORECASE)
    print("Inserted Chapter 9 <ol> successfully!")
else:
    print("Warning: Chapter 9 header pattern not matched!")

with open('chapters/chapter_09.html', 'w', encoding='utf-8') as f:
    f.write(ch9_html)


# 2. Fix Chapter 11
with open('chapters/chapter_11.html', 'r', encoding='utf-8') as f:
    ch11_html = f.read()

# Replace exact broken lines 55-56 and 518-519
ch11_html = re.sub(
    r'<a href="&lt;a href=" https:="" splitrockenvironmental\.ca""="">https://splitrockenvironmental\.ca</a>/products/big-sagebrush-"&gt;\s*<a href="https://splitrockenvironmental\.ca">https://splitrockenvironmental\.ca</a>/products/big-sagebrush-',
    '<a href="https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294">https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294</a>',
    ch11_html
)

ch11_html = re.sub(
    r'<a href="&lt;a href=" https:="" splitrockenvironmental\.ca""="">https://splitrockenvironmental\.ca</a>/products/big-sagebrush-kawkwu\?variant=40347062960294"&gt;\s*<a href="https://splitrockenvironmental\.ca">https://splitrockenvironmental\.ca</a>/products/big-sagebrush-kawkwu\?variant=40347062960294',
    '<a href="https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294">https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294</a>',
    ch11_html
)

with open('chapters/chapter_11.html', 'w', encoding='utf-8') as f:
    f.write(ch11_html)
print("Chapter 11 malformed hrefs fixed successfully!")
