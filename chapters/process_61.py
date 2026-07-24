import re

def process_file():
    with open('C:/Users/DELL/Documents/antigravity/bold-hawking/chapters/chapter_61.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace captions
    captions = {
        'Fig 61.2: [CAPTION_PLACEHOLDER]': 'Fig 61.2: Botanical illustration of Shrubby Penstemon leaves and floral structures.',
        'Fig 61.1: [CAPTION_PLACEHOLDER]': 'Fig 61.1: Photograph of Shrubby Penstemon (<em>Penstemon fruticosus</em>) showing its characteristic tubular flowers.',
        'Fig 61.3: [CAPTION_PLACEHOLDER]': 'Fig 61.3: Chemical structure of Catalpol, a major iridoid glycoside found in Penstemon species.',
        'Fig 61.4: [CAPTION_PLACEHOLDER]': 'Fig 61.4: Chemical structure of Penstemoside, an iridoid glucoside characteristic to the Penstemon genus.',
        'Fig 61.5: [CAPTION_PLACEHOLDER]': 'Fig 61.5: Chemical structure of Verbascoside, a major phenylpropanoid glycoside.'
    }
    for old, new in captions.items():
        content = content.replace(old, new)

    # 2. Add superscripts
    replacements = [
        ("near the mouth.", "near the mouth.<sup>[11], [12]</sup>"),
        ("relieved pain quickly.", "relieved pain quickly.<sup>[1]</sup>"),
        ("prevent infection.", "prevent infection.<sup>[1]</sup>"),
        ("Primary Bioactive Compounds)", "Primary Bioactive Compounds)<sup>[2], [6]</sup>"),
        ("inhibition of inflammatory pathways", "inhibition of inflammatory pathways<sup>[10]</sup>"),
        ("Pain-relieving properties", "Pain-relieving properties<sup>[10]</sup>"),
        ("Broad-spectrum antibacterial activity", "Broad-spectrum antibacterial activity<sup>[3]</sup>"),
        ("Protects nervous system tissues", "Protects nervous system tissues<sup>[9]</sup>"),
        ("Supporting Compounds)", "Supporting Compounds)<sup>[7]</sup>"),
        ("Major phenylpropanoid", "Major phenylpropanoid<sup>[4]</sup>"),
        ("COX enzyme inhibition reducing prostaglandin synthesis", "COX enzyme inhibition reducing prostaglandin synthesis<sup>[10]</sup>"),
        ("Modulation of pain neurotransmitter pathways", "Modulation of pain neurotransmitter pathways<sup>[10]</sup>"),
        ("Anti-inflammatory effects reducing pain signals", "Anti-inflammatory effects reducing pain signals<sup>[10]</sup>"),
        ("Direct analgesic properties", "Direct analgesic properties<sup>[4]</sup>"),
        ("Neuroprotective effects on pain receptors", "Neuroprotective effects on pain receptors<sup>[4]</sup>"),
        ("Antioxidant protection of nerve tissues", "Antioxidant protection of nerve tissues<sup>[4]</sup>"),
        ("Anti-inflammatory effects in respiratory tract", "Anti-inflammatory effects in respiratory tract<sup>[10]</sup>"),
        ("Immune system modulation", "Immune system modulation<sup>[10]</sup>"),
        ("Antimicrobial activity against respiratory pathogens", "Antimicrobial activity against respiratory pathogens<sup>[3]</sup>"),
        ("Antioxidant protection of respiratory tissues", "Antioxidant protection of respiratory tissues<sup>[4]</sup>"),
        ("Enhanced immune response", "Enhanced immune response<sup>[4]</sup>"),
        ("Reduced inflammation in airways", "Reduced inflammation in airways<sup>[4]</sup>"),
        ("Local anesthetics through nerve signal blockade", "Local anesthetics through nerve signal blockade<sup>[10]</sup>"),
        ("Anti-inflammatory agents reducing dental inflammation", "Anti-inflammatory agents reducing dental inflammation<sup>[10]</sup>"),
        ("Antimicrobials preventing oral infections", "Antimicrobials preventing oral infections<sup>[3]</sup>"),
        ("Direct analgesic effects on dental nerves", "Direct analgesic effects on dental nerves<sup>[4]</sup>"),
        ("Anti-inflammatory action in gum tissues", "Anti-inflammatory action in gum tissues<sup>[4]</sup>"),
        ("Antimicrobial protection", "Antimicrobial protection<sup>[3]</sup>"),
        ("Anti-inflammatory effects reducing skin irritation", "Anti-inflammatory effects reducing skin irritation<sup>[10]</sup>"),
        ("Antimicrobial protection against skin pathogens", "Antimicrobial protection against skin pathogens<sup>[3]</sup>"),
        ("Enhanced wound healing", "Enhanced wound healing<sup>[10]</sup>"),
        ("Antioxidant protection of skin cells", "Antioxidant protection of skin cells<sup>[4]</sup>"),
        ("Anti-inflammatory effects", "Anti-inflammatory effects<sup>[4]</sup>"),
        ("Improved skin barrier function", "Improved skin barrier function<sup>[4]</sup>"),
        ("Reduced tissue inflammation → Pain relief", "Reduced tissue inflammation → Pain relief<sup>[10]</sup>"),
        ("Anti-inflammatory and analgesic effects", "Anti-inflammatory and analgesic effects<sup>[10]</sup>"),
        ("Enhanced pain threshold → Reduced pain perception", "Enhanced pain threshold → Reduced pain perception<sup>[10]</sup>"),
        ("Pain neurotransmission → Localized pain relief", "Pain neurotransmission → Localized pain relief<sup>[4]</sup>"),
        ("ATP leakage → Cell death", "ATP leakage → Cell death<sup>[3]</sup>"),
        ("Metabolic disruption → Growth inhibition → Reduced infection", "Metabolic disruption → Growth inhibition → Reduced infection<sup>[3]</sup>"),
        ("Enhanced neuronal survival → Neuroprotection → Improved nerve function", "Enhanced neuronal survival → Neuroprotection → Improved nerve function<sup>[9]</sup>"),
        ("Protected nerve tissues → Reduced pain signals", "Protected nerve tissues → Reduced pain signals<sup>[9]</sup>"),
        ("Stable radical species + H₂O", "Stable radical species + H₂O<sup>[4]</sup>"),
        ("Enhanced cellular defense mechanisms", "Enhanced cellular defense mechanisms<sup>[9]</sup>"),
        ("Traditional Preparation Methods and Biochemical Optimization", "Traditional Preparation Methods and Biochemical Optimization<sup>[1]</sup>"),
        ("Cultural and Ecological Significance", "Cultural and Ecological Significance<sup>[1], [11]</sup>"),
        ("Safety Considerations and Traditional Wisdom", "Safety Considerations and Traditional Wisdom<sup>[1], [10]</sup>")
    ]
    for old, new in replacements:
        content = content.replace(old, new)

    # 3. Replace references section
    refs_html = '''  <p>
   <span style="color: #339966">
    <strong>
     References
    </strong>
   </span>
  </p>
  <p>
   1. Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.).
  </p>
  <p>
   2. Gering, B., Junior, P., &amp; Wichtl, M. (1987). Iridoid glycosides from <em>Penstemon confertus</em>. <em>Phytochemistry, 26</em>(11), 3011–3013. <a href="https://doi.org/10.1016/S0031-9422(00)82276-8">https://doi.org/10.1016/S0031-9422(00)82276-8</a>
  </p>
  <p>
   3. Hernández, T., Canales, M., &amp; Avila, J. G. (2012). Chemical analysis and antimicrobial activity of <em>Penstemon campanulatus</em>. <em>Natural Product Research, 26</em>(15), 1424–1431. <a href="https://doi.org/10.1080/14786419.2011.567434">https://doi.org/10.1080/14786419.2011.567434</a>
  </p>
  <p>
   4. Isacchi, B., Faniello, M. C., &amp; Bilia, A. R. (2011). Antihyperalgesic activity of verbascoside in two models of neuropathic pain. <em>Journal of Pharmacy and Pharmacology, 63</em>(4), 594–601. <a href="https://doi.org/10.1111/j.2042-7158.2011.01257.x">https://doi.org/10.1111/j.2042-7158.2011.01257.x</a>
  </p>
  <p>
   5. Jensen, S. R., &amp; Nielsen, B. J. (1981). Iridoid and other glycosides from <em>Penstemon</em>. <em>Phytochemistry, 20</em>(12), 2753–2756. <a href="https://doi.org/10.1016/0031-9422(81)80031-U">https://doi.org/10.1016/0031-9422(81)80031-U</a>
  </p>
  <p>
   6. Jensen, S. R., &amp; Nielsen, B. J. (1992). Iridoid glycosides from <em>Penstemon</em> species: A C-5, C-9 trans iridoid. <em>Phytochemistry, 31</em>(11), 3921–3924. <a href="https://doi.org/10.1016/0031-9422(92)80441-G">https://doi.org/10.1016/0031-9422(92)80441-G</a>
  </p>
  <p>
   7. Jensen, S. R., &amp; Olsen, C. E. (1995). Verbascoside derivatives and iridoid glycosides from <em>Penstemon crandallii</em>. <em>Phytochemistry, 40</em>(5), 1459–1463. <a href="https://doi.org/10.1016/0031-9422(95)00077-J">https://doi.org/10.1016/0031-9422(95)00077-J</a>
  </p>
  <p>
   8. Jensen, S. R., &amp; Olsen, C. E. (1999). Trans-fused iridoid glycosides from <em>Penstemon mucronatus</em>. <em>Phytochemistry, 51</em>(3), 387–390. <a href="https://doi.org/10.1016/S0031-9422(99)00003-6">https://doi.org/10.1016/S0031-9422(99)00003-6</a>
  </p>
  <p>
   9. Jiang, B., Shen, J., Chen, Q., Ding, J., Cheng, Q., Lu, J., &amp; Wang, Q. (2015). Catalpol promotes neurogenesis and inhibits apoptosis of newborn neurons. <em>Frontiers in Pharmacology, 6</em>, 230. <a href="https://doi.org/10.3389/fphar.2015.00230">https://doi.org/10.3389/fphar.2015.00230</a>
  </p>
  <p>
   10. Viljoen, A. M., Mncwangi, N., &amp; Vermaak, I. (2014). Anti-inflammatory iridoids of botanical origin. <em>Phytochemistry Letters, 10</em>, xxi–xxix. <a href="https://doi.org/10.1016/j.phytol.2014.06.004">https://doi.org/10.1016/j.phytol.2014.06.004</a>
  </p>
  <p>
   11. Washington Native Plant Society. (2025). <em>Penstemon fruticosus</em>. <a href="https://www.wnps.org/native-plant-directory/331:penstemon-fruticosus">https://www.wnps.org/native-plant-directory/331:penstemon-fruticosus</a>
  </p>
  <p>
   12. Wikipedia contributors. (2024, December 7). <em>Penstemon fruticosus</em>. In <em>Wikipedia, The Free Encyclopedia</em>. <a href="https://en.wikipedia.org/wiki/Penstemon_fruticosus">https://en.wikipedia.org/wiki/Penstemon_fruticosus</a>
  </p>
 </section>'''

    content = re.sub(r'<p>\s*<span style="color: #339966">\s*<strong>\s*References\s*</strong>\s*</span>\s*</p>.*?</section>', refs_html, content, flags=re.DOTALL)
    
    with open('C:/Users/DELL/Documents/antigravity/bold-hawking/chapters/chapter_61.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    process_file()
