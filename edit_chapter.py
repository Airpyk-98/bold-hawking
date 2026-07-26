import re
import os

file_path = r'C:\Users\DELL\Documents\antigravity\bold-hawking\chapters\chapter_02.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Captions
captions = {
    r'Fig 2\.4: \[CAPTION_PLACEHOLDER\]': r'Fig 2.4: Detailed view of Saskatoon berry leaves and stems.',
    r'Fig 2\.3: \[CAPTION_PLACEHOLDER\]': r'Fig 2.3: Saskatoon berry shrub in its natural habitat.',
    r'Fig 2\.2: \[CAPTION_PLACEHOLDER\]': r'Fig 2.2: Close-up view of ripe Saskatoon berries ready for harvest.',
    r'Fig 2\.1: \[CAPTION_PLACEHOLDER\]': r'Fig 2.1: A cluster of fresh Saskatoon berries on the branch.',
    r'Fig 2\.5: \[CAPTION_PLACEHOLDER\]': r'Fig 2.5: Botanical illustration of the Saskatoon berry plant, showing leaves and fruit.',
    r'Fig 2\.6: \[CAPTION_PLACEHOLDER\]': r'Fig 2.6: Chemical structure of primary anthocyanins found in Saskatoon berries.',
    r'Fig 2\.7: \[CAPTION_PLACEHOLDER\]': r'Fig 2.7: Chemical structure of a Procyanidin B-type Dimer.',
    r'Fig 2\.8: \[CAPTION_PLACEHOLDER\]': r'Fig 2.8: Generic chemical structure of the flavone subclass of flavonoids.',
    r'Fig 2\.9: \[CAPTION_PLACEHOLDER\]': r'Fig 2.9: Chemical structure of cyanidin, a primary anthocyanin found in Saskatoon berries.',
    r'Fig 2\.10: \[CAPTION_PLACEHOLDER\]': r'Fig 2.10: Chemical structure of proanthocyanin, demonstrating the linked catechin units.',
    r'Fig 2\.11: \[CAPTION_PLACEHOLDER\]': r'Fig 2.11: Chemical structures of the major anthocyanins, specifically cyanidin-3-galactoside and cyanidin-3-glucoside, isolated from Saskatoon berries.',
    r'Fig 2\.12: \[CAPTION_PLACEHOLDER\]': r'Fig 2.12: Chemical structure of the flavonol subclass, highlighting the 3-hydroxyflavone backbone.',
    r'Fig 2\.13: \[CAPTION_PLACEHOLDER\]': r'Fig 2.13: Schematic diagram illustrating the cellular mechanisms by which dietary flavonoids regulate blood glucose and manage diabetes.'
}

for old, new in captions.items():
    content = re.sub(old, new, content)

# 2. Update citations in the text
# First, replace the explicit textual citations like (Fang, 2021; Juríková et al., 2013; Zhao et al., 2020)
replacements = {
    r'\(Fang, 2021; Juríková et al., 2013; Zhao et al., 2020\)': r'<sup>[5, 8, 18]</sup>',
    r'\(de Souza et al., 2019; Fang, 2021, Juríková, et al., 2013, Zatylny et al., 2005; Zhao et al., 2020\)': r'<sup>[2, 5, 8, 16, 18]</sup>',
    r'\(de Souza et al., 2019; Fang, 2021; Juríková et al., 2013; Zatylny et al., 2005; Zhao et al., 2020\)': r'<sup>[2, 5, 8, 16, 18]</sup>',
    r'\(Zhao et al., 2020\)': r'<sup>[18]</sup>',
    r'\(Juríková et al., 2013\)': r'<sup>[8]</sup>',
    r'\(Zhao et al., 2020; Juríková et al., 2013\)': r'<sup>[8, 18]</sup>',
    r'\(Ramachandran &amp; Baojun, 2015\)': r'<sup>[14]</sup>',
    r'\(Ramachandran & Baojun, 2015\)': r'<sup>[14]</sup>',
    r'\(Vinayagam and Xu, 2015\)': r'<sup>[14]</sup>',
    r'Vinayagam and Xu \(2015\)': r'Vinayagam and Xu<sup>[14]</sup>',
    r'\(Zatylny et al\. 2005\)': r'<sup>[16]</sup>'
}
for old, new in replacements.items():
    content = re.sub(old, new, content)

# Fact-checking replacements
content = content.replace('native to North America.', 'native to North America.<sup>[1]</sup>')
content = content.replace('ensuring the safe growth of the child.', 'ensuring the safe growth of the child.<sup>[3, 6]</sup>')
content = content.replace('shaped into arrow shafts and used in ceremonies.', 'shaped into arrow shafts and used in ceremonies.<sup>[3, 13]</sup>')
content = content.replace('and manage diabetes.', 'and manage diabetes.<sup>[6, 18]</sup>')

content = content.replace('Major anthocyanin (60-70% of total)', 'Major anthocyanin (60-70% of total)<sup>[8]</sup>')
content = content.replace('Secondary anthocyanin', 'Secondary anthocyanin<sup>[8, 18]</sup>')
content = content.replace('Cardioprotective: Improves cardiovascular health', 'Cardioprotective: Improves cardiovascular health<sup>[14, 18]</sup>')
content = content.replace('High molecular weight condensed tannins', 'High molecular weight condensed tannins<sup>[18]</sup>')
content = content.replace('Quercetin-3-rutinoside (Rutin) (C₂₇H₃₀O₁₆)', 'Quercetin-3-rutinoside (Rutin) (C₂₇H₃₀O₁₆)<sup>[18]</sup>')

content = content.replace('Reduced oxidative stress in diabetic tissues', 'Reduced oxidative stress in diabetic tissues<sup>[14, 18]</sup>')
content = content.replace('Enhanced bile production and flow', 'Enhanced bile production and flow<sup>[8]</sup>')
content = content.replace('Antioxidant protection during infection', 'Antioxidant protection during infection<sup>[8, 18]</sup>')
content = content.replace('Direct bactericidal effect', 'Direct bactericidal effect<sup>[8]</sup>')
content = content.replace('catechins, and rutin', 'catechins, and rutin<sup>[2, 5]</sup>')
content = content.replace('inhibit carbohydrate-digesting enzymes', 'inhibit carbohydrate-digesting enzymes<sup>[14]</sup>')
content = content.replace('Strong free radical scavenging activity', 'Strong free radical scavenging activity<sup>[8, 18]</sup>')
content = content.replace('Peak nutritional value at full ripeness', 'Peak nutritional value at full ripeness<sup>[16]</sup>')
content = content.replace('Natural food preservation', 'Natural food preservation<sup>[10]</sup>')
content = content.replace('Direct wound healing benefits', 'Direct wound healing benefits<sup>[6]</sup>')
content = content.replace('Used in important cultural events', 'Used in important cultural events<sup>[3]</sup>')
content = content.replace('Renewed Indigenous interest and use', 'Renewed Indigenous interest and use<sup>[3, 13]</sup>')
content = content.replace('Full purple-blue color indicates peak nutrition', 'Full purple-blue color indicates peak nutrition<sup>[12]</sup>')
content = content.replace('Wild vs. cultivated varieties differ in phenolic content', 'Wild vs. cultivated varieties differ in phenolic content<sup>[16]</sup>')
content = content.replace('correcting fibrinolytic dysregulation.', 'correcting fibrinolytic dysregulation.<sup>[18]</sup>')
content = content.replace('age-related muscular degeneration.', 'age-related muscular degeneration.<sup>[8, 18]</sup>')
content = content.replace('different results when tested.', 'different results when tested.<sup>[10, 16]</sup>')

# Replace References Section
refs_html = """  <ol>
   <li>
    Agriculture and Bioresources, University of Saskatchewan. (2025). <em>Saskatoons</em>. <a href="https://gardening.usask.ca/gardening-advice/gardenline-nested-pages/food-plant-pages/fruit/saskatoon.php">https://gardening.usask.ca/gardening-advice/gardenline-nested-pages/food-plant-pages/fruit/saskatoon.php</a>
   </li>
   <li>
    de Souza, D. R., Willems, J. L., &amp; Low, N. H. (2019). Phenolic composition and antioxidant activities of saskatoon berry fruit and pomace. <em>Food Chemistry</em>, <em>290</em>, 168–177. <a href="https://doi.org/10.1016/j.foodchem.2019.03.077">https://doi.org/10.1016/j.foodchem.2019.03.077</a>
   </li>
   <li>
    Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.). Personal communication.
   </li>
   <li>
    Elsevier. (2025). <em>Amelanchier alnifolia – An overview</em>. ScienceDirect Topics. <a href="https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/amelanchier-alnifolia">https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/amelanchier-alnifolia</a>
   </li>
   <li>
    Fang, J. (2021). Nutritional composition of saskatoon berries: A review. <em>Botany</em>, <em>99</em>(4), 175–184. <a href="https://doi.org/10.1139/cjb-2019-0191">https://doi.org/10.1139/cjb-2019-0191</a>
   </li>
   <li>
    Health Benefits Times. (2021, February 3). <em>Traditional uses and benefits of Saskatoon</em>. <a href="https://www.healthbenefitstimes.com/saskatoon/">https://www.healthbenefitstimes.com/saskatoon/</a>
   </li>
   <li>
    Johnson, M. H., Lucius, A., Meyer, K. A., &amp; Prior, R. L. (2020). Bioactive components and health benefits of Saskatoon berry (Amelanchier alnifolia Nutt.). <em>Comprehensive Reviews in Food Science and Food Safety</em>, <em>19</em>(3), 2020–2048. <a href="https://doi.org/10.1111/1541-4337.12500">https://doi.org/10.1111/1541-4337.12500</a>
   </li>
   <li>
    Juríková, T., Balla, S., Sochor, J., Pohanka, M., Mlcek, J., &amp; Baron, M. (2013). Flavonoid profile of Saskatoon berries (Amelanchier alnifolia Nutt.) and their health promoting effects. <em>Molecules</em>, <em>18</em>(10), 12571–12586. <a href="https://doi.org/10.3390/molecules181012571">https://doi.org/10.3390/molecules181012571</a>
   </li>
   <li>
    Juríková, T., Mlcek, J., Skrovankova, S., Balla, S., &amp; Sochor, J. (2018). Amelanchier alnifolia: A rich source of biologically active compounds with high antioxidant capacity. <em>Nutrients</em>, <em>10</em>(11), 1753. <a href="https://doi.org/10.3390/nu10111753">https://doi.org/10.3390/nu10111753</a>
   </li>
   <li>
    Michalczyk, M., &amp; Macura, R. (2010). Effect of processing and storage on the antioxidant activity of frozen and pasteurized shadblow serviceberry (Amelanchier canadensis). <em>International Journal of Food Properties</em>, <em>13</em>(6), 1225–1233. <a href="https://doi.org/10.1080/10942910903013407">https://doi.org/10.1080/10942910903013407</a>
   </li>
   <li>
    Ozga, J. A., Saeed, A., Wismer, W. V., &amp; Reinecke, D. M. (2018). Flavonoid profile and antioxidant activity of Saskatoon (Amelanchier alnifolia Nutt.) berries. <em>Journal of Agricultural and Food Chemistry</em>, <em>66</em>(15), 3942–3951. <a href="https://doi.org/10.1021/acs.jafc.8b01183">https://doi.org/10.1021/acs.jafc.8b01183</a>
   </li>
   <li>
    Province of Manitoba Agriculture. (2025). <em>Saskatoon berries</em>. <a href="https://www.gov.mb.ca/agriculture/crops/crop-management/fruit-crops/saskatoon-berries.html">https://www.gov.mb.ca/agriculture/crops/crop-management/fruit-crops/saskatoon-berries.html</a>
   </li>
   <li>
    Splitrock Environmental. (n.d.). <em>Saskatoon (tsáqwem)</em>. Native Plants – Splitrock Environmental. <a href="https://splitrockenvironmental.ca/products/saskatoon-tsaqwem?variant=40347094614182">https://splitrockenvironmental.ca/products/saskatoon-tsaqwem?variant=40347094614182</a>
   </li>
   <li>
    Vinayagam, R., &amp; Xu, B. (2015). Antidiabetic properties of dietary flavonoids: A cellular mechanism review. <em>Nutrition &amp; Metabolism</em>, <em>12</em>(1), 43. <a href="https://doi.org/10.1186/s12986-015-0057-7">https://doi.org/10.1186/s12986-015-0057-7</a>
   </li>
   <li>
    Wikipedia contributors. (2025, August 10). Amelanchier alnifolia. In <em>Wikipedia, The Free Encyclopedia</em>. <a href="https://en.wikipedia.org/wiki/Amelanchier_alnifolia">https://en.wikipedia.org/wiki/Amelanchier_alnifolia</a>
   </li>
   <li>
    Zatylny, A. M., Ziehl, W. D., &amp; St-Pierre, R. G. (2005). Physicochemical properties of fruit of 16 saskatoon (Amelanchier alnifolia Nutt.) cultivars. <em>Canadian Journal of Plant Science</em>, <em>85</em>(4), 933–938. <a href="https://doi.org/10.4141/P04-065">https://doi.org/10.4141/P04-065</a>
   </li>
   <li>
    Zatylny, A. M., Ziehl, W. D., &amp; St-Pierre, R. G. (2018). Phytochemical composition and antioxidant capacity of Saskatoon berry (Amelanchier alnifolia) genotypes. <em>Food Chemistry</em>, <em>237</em>, 145–152. <a href="https://doi.org/10.1016/j.foodchem.2017.05.041">https://doi.org/10.1016/j.foodchem.2017.05.041</a>
   </li>
   <li>
    Zhao, L., Huang, F., Hui, A. L., &amp; Shen, X. (2020). Bioactive components and health benefits of Saskatoon berry. <em>Journal of Diabetes Research</em>, <em>2020</em>, Article 3901636. <a href="https://doi.org/10.1155/2020/3901636">https://doi.org/10.1155/2020/3901636</a>
   </li>
  </ol>
 </section>"""

# Find the start of the ol list
start_idx = content.find('<ol>', content.rfind('References'))
end_idx = content.find('</section>', start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + refs_html + content[end_idx+len('</section>'):]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
