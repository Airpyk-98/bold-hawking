import re

file_path = r'C:\Users\DELL\Documents\antigravity\bold-hawking\chapters\chapter_45.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Captions
content = content.replace('Fig 45.1: [CAPTION_PLACEHOLDER]', 'Fig 45.1: Mountain Alder (Alnus incana) leaves, showcasing the characteristic oval shape and doubly serrated margins.')
content = content.replace('Fig 45.2: [CAPTION_PLACEHOLDER]', 'Fig 45.2: Close-up of Mountain Alder branches and foliage, highlighting its thinleaf traits and growth habit.')
content = content.replace('Fig 45.3: [CAPTION_PLACEHOLDER]', 'Fig 45.3: Illustration or detailed view of Mountain Alder, a deciduous shrub vital to riparian restoration.')
content = content.replace('Fig 45.4: [CAPTION_PLACEHOLDER]', 'Fig 45.4: Chemical structure of Betulinic Acid, a pentacyclic lupane triterpene noted for its anti-mycobacterial properties.')
content = content.replace('Fig 45.5: [CAPTION_PLACEHOLDER]', 'Fig 45.5: Chemical structure of Betulone, an oxidized triterpene contributing to the medicinal efficacy of Mountain Alder.')

# Citations
replacements = [
    ("native to western North America.", "native to western North America.<sup>[1][11]</sup>"),
    ("enriching poor soils.", "enriching poor soils.<sup>[3]</sup>"),
    ("measuring 2-4 inches long.", "measuring 2-4 inches long.<sup>[1]</sup>"),
    ("dense thickets through root suckers and rhizomes.", "dense thickets through root suckers and rhizomes.<sup>[8]</sup>"),
    ("carried medicine in its bark and leaves.", "carried medicine in its bark and leaves.<sup>[2]</sup>"),
    ("relief to those struggling to breathe.", "relief to those struggling to breathe.<sup>[2][5]</sup>"),
    ("other irritations until the pain subsided.", "other irritations until the pain subsided.<sup>[4]</sup>"),
    ("rinse for mouth sores.", "rinse for mouth sores.<sup>[9]</sup>"),
    ("ease the discomfort of illness.", "ease the discomfort of illness.<sup>[4]</sup>"),
    ("sustenance were intertwined.", "sustenance were intertwined.<sup>[9]</sup>"),
    ("offering balance to the stomach.", "offering balance to the stomach.<sup>[4]</sup>"),
    ("keeping the mouth strong and healthy.", "keeping the mouth strong and healthy.<sup>[4][9]</sup>"),
    ("soothe infections and conjunctivitis.", "soothe infections and conjunctivitis.<sup>[2]</sup>"),
    ("prayers for cleansing and protection.", "prayers for cleansing and protection.<sup>[2]</sup>"),
    ("Primary Bioactive Compounds)\\n    </strong>", "Primary Bioactive Compounds)<sup>[5][6]</sup>\\n    </strong>"),
    ("Major bark triterpene (up to 25% dry weight)", "Major bark triterpene (up to 25% dry weight)<sup>[6]</sup>"),
    ("Anti-mycobacterial compound", "Anti-mycobacterial compound<sup>[5]</sup>"),
    ("Oxidized triterpene", "Oxidized triterpene<sup>[5]</sup>"),
    ("Mycobacterium tuberculosis\\n    </em>", "Mycobacterium tuberculosis\\n    </em><sup>[5]</sup>"),
    ("Strong inhibition of inflammatory pathways", "Strong inhibition of inflammatory pathways<sup>[12]</sup>"),
    ("Broad-spectrum antibacterial and antifungal activity", "Broad-spectrum antibacterial and antifungal activity<sup>[10]</sup>"),
    ("Enhances tissue repair and collagen synthesis", "Enhances tissue repair and collagen synthesis<sup>[6]</sup>"),
    ("Diarylheptanoids (Supporting Compounds)\\n    </strong>", "Diarylheptanoids (Supporting Compounds)<sup>[7]</sup>\\n    </strong>"),
    ("Major diarylheptanoid", "Major diarylheptanoid<sup>[7]</sup>"),
    ("Bioactive diarylheptanoid", "Bioactive diarylheptanoid<sup>[6]</sup>"),
    ("Similar structure + glucose moiety)", "Similar structure + glucose moiety)<sup>[7]</sup>"),
    ("Hydrolyzable Tannins (Astringent Compounds)\\n    </strong>", "Hydrolyzable Tannins (Astringent Compounds)<sup>[10]</sup>\\n    </strong>"),
    ("multiple galloyl units esterified to glucose core)", "multiple galloyl units esterified to glucose core)<sup>[10]</sup>"),
    ("Triterpenes (betulin, betulinic acid, betulone) act through:", "Triterpenes (betulin, betulinic acid, betulone) act through:<sup>[5]</sup>"),
    ("Diarylheptanoids contribute:", "Diarylheptanoids contribute:<sup>[7]</sup>"),
    ("Betulin and derivatives provide:", "Betulin and derivatives provide:<sup>[6][12]</sup>"),
    ("Tannins facilitate:", "Tannins facilitate:<sup>[10]</sup>"),
    ("Hydrolyzable tannins act as:", "Hydrolyzable tannins act as:<sup>[10]</sup>"),
    ("Triterpenes support:", "Triterpenes support:<sup>[6]</sup>"),
    ("Increased membrane permeability → ATP leakage → Cell death", "Increased membrane permeability → ATP leakage → Cell death<sup>[5]</sup>"),
    ("Impaired structural integrity → Growth arrest", "Impaired structural integrity → Growth arrest<sup>[5]</sup>"),
    ("Inhibited replication → Reduced bacterial load", "Inhibited replication → Reduced bacterial load<sup>[5]</sup>"),
    ("Reduced inflammation and tissue damage", "Reduced inflammation and tissue damage<sup>[12]</sup>"),
    ("Anti-inflammatory and analgesic effects", "Anti-inflammatory and analgesic effects<sup>[7]</sup>"),
    ("Improved tissue tensile strength → Faster healing", "Improved tissue tensile strength → Faster healing<sup>[6]</sup>"),
    ("Reduced fluid loss + Microbial protection → Optimal healing", "Reduced fluid loss + Microbial protection → Optimal healing<sup>[10]</sup>"),
    ("Reduced capillary permeability → Decreased inflammation", "Reduced capillary permeability → Decreased inflammation<sup>[10]</sup>"),
    ("Clot formation → Bleeding cessation", "Clot formation → Bleeding cessation<sup>[10]</sup>"),
    ("Ion leakage + ATP depletion → Cell death", "Ion leakage + ATP depletion → Cell death<sup>[6]</sup>"),
    ("Metabolic disruption → Growth inhibition", "Metabolic disruption → Growth inhibition<sup>[7]</sup>"),
    ("Optimizes triterpene and tannin extraction", "Optimizes triterpene and tannin extraction<sup>[6][10]</sup>"),
    ("Increases concentration of bioactive compounds", "Increases concentration of bioactive compounds<sup>[2]</sup>"),
    ("Traditional knowledge distinguishes potency differences", "Traditional knowledge distinguishes potency differences<sup>[2]</sup>"),
    ("Multiple daily doses for serious conditions like tuberculosis", "Multiple daily doses for serious conditions like tuberculosis<sup>[2]</sup>"),
    ("Maximum triterpene content for wound healing", "Maximum triterpene content for wound healing<sup>[2]</sup>"),
    ("Concentrated tannins for astringent effects", "Concentrated tannins for astringent effects<sup>[4]</sup>"),
    ("Bark + leaves for enhanced antimicrobial activity", "Bark + leaves for enhanced antimicrobial activity<sup>[9]</sup>"),
    ("ecological role enhances its medicinal significance:", "ecological role enhances its medicinal significance:<sup>[3]</sup>"),
    ("Nitrogen fixation creates nutrient-rich habitats", "Nitrogen fixation creates nutrient-rich habitats<sup>[1]</sup>"),
    ("Stabilizes stream banks and wetlands", "Stabilizes stream banks and wetlands<sup>[8]</sup>"),
    ("Colonizes disturbed areas, providing early resources", "Colonizes disturbed areas, providing early resources<sup>[11]</sup>"),
    ("Provides food and habitat for numerous species", "Provides food and habitat for numerous species<sup>[3]</sup>"),
    ("Indigenous practices emphasize:", "Indigenous practices emphasize:<sup>[2]</sup>"),
    ("Indigenous preparation methods include important safeguards:", "Indigenous preparation methods include important safeguards:<sup>[2]</sup>"),
    ("High levels may cause digestive upset if taken internally in excess", "High levels may cause digestive upset if taken internally in excess<sup>[10]</sup>"),
    ("Low oral bioavailability may require topical applications", "Low oral bioavailability may require topical applications<sup>[6]</sup>"),
    ("Proper species identification and bark preparation", "Proper species identification and bark preparation<sup>[4]</sup>"),
    ("Serious conditions like tuberculosis require medical oversight", "Serious conditions like tuberculosis require medical oversight<sup>[5]</sup>")
]

for old, new in replacements:
    content = content.replace(old, new)

references_html = '''<p>
  <span style="color: #339966">
   <strong>
    References
   </strong>
  </span>
 </p>
 <ol>
  <li>
   Calscape. (2025). <em>Mountain alder (Alnus incana ssp. tenuifolia).</em> <a href="https://calscape.org/Alnus-incana-ssp.-tenuifolia-(Mountain-Alder)" rel="noopener" target="_new">https://calscape.org/Alnus-incana-ssp.-tenuifolia-(Mountain-Alder)</a>
  </li>
  <li>
   Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.).
  </li>
  <li>
   Medicinal Forest Garden Trust. (2024, February 24). <em>Alder: Research notes.</em> <a href="https://medicinalforestgardentrust.org/alder-research-notes/" rel="noopener" target="_new">https://medicinalforestgardentrust.org/alder-research-notes/</a>
  </li>
  <li>
   Natural Medicinal Herbs. (2025). <em>Mountain alder (Alnus tenuifolia).</em> <a href="https://www.naturalmedicinalherbs.net/herbs/a/alnus-tenuifolia=mountain-alder.php" rel="noopener" target="_new">https://www.naturalmedicinalherbs.net/herbs/a/alnus-tenuifolia=mountain-alder.php</a>
  </li>
  <li>
   Nisbet, L. J., Hansen, J., &amp; Marles, R. J. (2015). Anti-mycobacterial triterpenes from the Canadian medicinal plant <em>Alnus incana</em>. <em>Journal of Ethnopharmacology, 165</em>, 148–151. <a href="https://doi.org/10.1016/j.jep.2015.02.044">https://doi.org/10.1016/j.jep.2015.02.044</a>
  </li>
  <li>
   Ren, D., Zuo, R., Guan, Y., Li, S., &amp; Guo, H. (2017). The genus <em>Alnus</em>: A comprehensive outline of its chemical constituents and biological activities. <em>Molecules, 22</em>(8), 1383. <a href="https://doi.org/10.3390/molecules22081383">https://doi.org/10.3390/molecules22081383</a>
  </li>
  <li>
   Sati, S. C., Sati, N., &amp; Sati, O. P. (2011). Bioactive constituents and medicinal importance of genus <em>Alnus</em>. <em>Pharmacognosy Reviews, 5</em>(10), 174–183. <a href="https://doi.org/10.4103/0973-7847.91118">https://doi.org/10.4103/0973-7847.91118</a>
  </li>
  <li>
   Sevenoaks Native Nursery. (2023, December 27). <em>Alnus incana ssp. tenuifolia.</em> <a href="https://sevenoaksnativenursery.com/product/alnus-incana-ssp-tenuifolia/" rel="noopener" target="_new">https://sevenoaksnativenursery.com/product/alnus-incana-ssp-tenuifolia/</a>
  </li>
  <li>
   Song of the Woods. (2025, February 7). <em>Alder – Alnus spp.: Edible and medicinal uses.</em> <a href="https://www.songofthewoods.com/alder-alnus-spp/" rel="noopener" target="_new">https://www.songofthewoods.com/alder-alnus-spp/</a>
  </li>
  <li>
   Tung, N. H., Ding, Y., Kim, S. K., &amp; Kim, Y. H. (2010). Total phenolic and flavonoid contents, antioxidant and antimicrobial activities of <em>Alnus</em> species. <em>African Journal of Pharmacy and Pharmacology, 4</em>(8), 515–520. <a href="https://academicjournals.org/journal/AJPP/article-full-text-pdf/6B9BE9D21626">https://academicjournals.org/journal/AJPP/article-full-text-pdf/6B9BE9D21626</a>
  </li>
  <li>
   Wikipedia. (2025, June 5). <em>Alnus incana</em>. <a href="https://en.wikipedia.org/wiki/Alnus_incana" rel="noopener" target="_new">https://en.wikipedia.org/wiki/Alnus_incana</a>
  </li>
  <li>
   Yogeeswari, P., &amp; Sriram, D. (2005). Betulinic acid and its derivatives: A review on their biological properties. <em>Current Medicinal Chemistry, 12</em>(6), 657–666. <a href="https://doi.org/10.2174/0929867053202214">https://doi.org/10.2174/0929867053202214</a>
  </li>
 </ol>
</section>'''

content = re.sub(r'<p>\s*<span style="color: #339966">\s*<strong>\s*References\s*</strong>\s*</span>\s*</p>.*?</section>', references_html, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete.")
