import re

with open('chapter_32.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Fig 32.5: [CAPTION_PLACEHOLDER]', 'Fig 32.5: Full tree view of the Douglas Maple')
content = content.replace('Fig 32.4: [CAPTION_PLACEHOLDER]', 'Fig 32.4: Branches and twigs of the Douglas Maple')
content = content.replace('Fig 32.3: [CAPTION_PLACEHOLDER]', 'Fig 32.3: Seeds (samaras) of the Douglas Maple')
content = content.replace('Fig 32.2: [CAPTION_PLACEHOLDER]', 'Fig 32.2: Bark of the Douglas Maple')
content = content.replace('Fig 32.1: [CAPTION_PLACEHOLDER]', 'Fig 32.1: Leaves of the Douglas Maple (*Acer glabrum*)')
content = content.replace('Fig 32.7: [CAPTION_PLACEHOLDER]', 'Fig 32.7: Douglas Maple in its natural habitat')
content = content.replace('Fig 32.6: [CAPTION_PLACEHOLDER]', 'Fig 32.6: Detailed view of the Douglas Maple leaves')
content = content.replace('Fig 32.8: [CAPTION_PLACEHOLDER]', 'Fig 32.8: Chemical Structure of Hydrolyzable Tannins')
content = content.replace('Fig 32.9: [CAPTION_PLACEHOLDER]', 'Fig 32.9: General Structure of Saponins')

content = content.replace(
    'Douglas Maple represents an important traditional medicine with validated pharmacological properties. Its traditional uses by Indigenous peoples, particularly for digestive issues and inflammation, are supported by its rich phytochemical profile containing tannins, saponins, and flavonoids.',
    'Douglas Maple represents an important traditional medicine with validated pharmacological properties. Its traditional uses by Indigenous peoples, particularly for digestive issues and inflammation, are supported by its rich phytochemical profile containing tannins, saponins, and flavonoids.<sup>[3]</sup>'
)

content = content.replace(
    'The biochemical mechanisms underlying its medicinal properties involve anti-inflammatory pathways, antimicrobial activity, and astringent effects that align with traditional applications.',
    'The biochemical mechanisms underlying its medicinal properties involve anti-inflammatory pathways, antimicrobial activity, and astringent effects that align with traditional applications.<sup>[3]</sup>'
)

content = content.replace(
    'When sickness took hold and the stomach was unsettled, the bark or leaves were steeped into a tea to calm the bowels and ease diarrhea.',
    'When sickness took hold and the stomach was unsettled, the bark or leaves were steeped into a tea to calm the bowels and ease diarrhea.<sup>[4][7][8]</sup>'
)

content = content.replace(
    'This medicine worked gently, cleansing without harm, and was often shared with those who had been weakened by long illness.',
    'This medicine worked gently, cleansing without harm, and was often shared with those who had been weakened by long illness.<sup>[4]</sup>'
)

content = content.replace(
    'The same infusions soothed swellings and inflammation throughout the body, cooling what had become hot or sore.',
    'The same infusions soothed swellings and inflammation throughout the body, cooling what had become hot or sore.<sup>[4]</sup>'
)

content = content.replace(
    'The inner bark was carefully prepared as a wash for sore or infected eyes.',
    'The inner bark was carefully prepared as a wash for sore or infected eyes.<sup>[4]</sup>'
)

content = content.replace(
    'A tea made from its parts was drunk as a renewal remedy, helping the people through the transitions between seasons when illness often visited the community.',
    'A tea made from its parts was drunk as a renewal remedy, helping the people through the transitions between seasons when illness often visited the community.<sup>[4]</sup>'
)

content = content.replace(
    'Its stems and wood were prized for their strength and flexibility, used to make snowshoe frames, bows, and tools that carried the people through winter and travel.',
    'Its stems and wood were prized for their strength and flexibility, used to make snowshoe frames, bows, and tools that carried the people through winter and travel.<sup>[4][7][8]</sup>'
)

content = content.replace(
    'Properties: Phenolics are ubiquitous compounds found in all plants as their secondary metabolites. These include simple phenols, hydroxybenzoic acid and cinnamic acid derivatives, flavonoids, coumarines and tannins, among others.',
    'Properties: Phenolics are ubiquitous compounds found in all plants as their secondary metabolites. These include simple phenols, hydroxybenzoic acid and cinnamic acid derivatives, flavonoids, coumarines and tannins, among others.<sup>[2]</sup>'
)

content = content.replace(
    'Function: Saponins are bioactive compounds generally considered to be produced by plants to counteract pathogens and herbivores. Besides their role in plant defense, saponins are of growing interest for drug research as they are active constituents of several folk medicines.',
    'Function: Saponins are bioactive compounds generally considered to be produced by plants to counteract pathogens and herbivores. Besides their role in plant defense, saponins are of growing interest for drug research as they are active constituents of several folk medicines.<sup>[1]</sup>'
)

content = content.replace(
    'Antioxidant Properties: Free radical scavenging activity',
    'Antioxidant Properties: Free radical scavenging activity<sup>[3]</sup>'
)

content = content.replace(
    'Modulation of inflammatory cytokines\n  </li>',
    'Modulation of inflammatory cytokines<sup>[3]</sup>\n  </li>'
)

content = content.replace(
    'Antimicrobial effects\n  </li>',
    'Antimicrobial effects<sup>[2]</sup>\n  </li>'
)

content = content.replace(
    'Chelation of metal ions required for microbial growth\n  </li>',
    'Chelation of metal ions required for microbial growth<sup>[1]</sup>\n  </li>'
)

content = content.replace(
    'Used for internal consumption\n    </li>',
    'Used for internal consumption<sup>[6][8]</sup>\n    </li>'
)

content = content.replace(
    'Poultices for swellings and inflammation\n    </li>',
    'Poultices for swellings and inflammation<sup>[6][8]</sup>\n    </li>'
)

content = content.replace(
    'Standardized for tannin content\n    </li>',
    'Standardized for tannin content<sup>[6]</sup>\n    </li>'
)

content = content.replace(
    'Not recommended during pregnancy without professional guidance\n  </li>',
    'Not recommended during pregnancy without professional guidance<sup>[3][6]</sup>\n  </li>'
)

content = content.replace(
    'Potential interaction with blood-thinning medications due to salicylate-like compounds\n  </li>',
    'Potential interaction with blood-thinning medications due to salicylate-like compounds<sup>[3][6]</sup>\n  </li>'
)

new_refs = """ <p>
  1. Augustin, J. M., Kuzina, V., Andersen, S. B., &amp; Bak, S. (2011). Molecular activities, biosynthesis and evolution of triterpenoid saponins. <em>Phytochemistry</em>, <em>72</em>(6), 435&ndash;457. <a href="https://doi.org/10.1016/j.phytochem.2011.01.015">https://doi.org/10.1016/j.phytochem.2011.01.015</a>
 </p>
 <p>
  2. Bate-Smith, E. C. (1977). Astringent tannins of <em>Acer</em>. <em>Phytochemistry</em>, <em>16</em>(9), 1421&ndash;1426. <a href="https://doi.org/10.1016/S0031-9422(00)88795-6">https://doi.org/10.1016/S0031-9422(00)88795-6</a>
 </p>
 <p>
  3. Bi, W., Gao, Y., Shen, J., He, C., Liu, H., Peng, Y., Zhang, C., &amp; Xiao, P. (2016). Traditional uses, phytochemistry, and pharmacology of the genus <em>Acer</em> (maple): A review. <em>Journal of Ethnopharmacology</em>, <em>189</em>, 31&ndash;60. <a href="https://doi.org/10.1016/j.jep.2016.04.021">https://doi.org/10.1016/j.jep.2016.04.021</a>
 </p>
 <p>
  4. Elders and Community members of the Cayoose Creek Band of Sekw&rsquo;el&rsquo;was. (n.d.). <em>Traditional knowledge and uses of Douglas Maple</em>.
 </p>
 <p>
  5. Evans, T. T. (2022). The Indigenous origins of maple syrup. <em>American Indian Magazine</em>. <a href="https://www.americanindianmagazine.org/Indigenous-origins-of-maple-syrup" rel="noopener" target="_blank">https://www.americanindianmagazine.org/Indigenous-origins-of-maple-syrup</a>
 </p>
 <p>
  6. Grieve, M. (n.d.). Maples. In <em>A modern herbal</em>. Botanical.com. <a href="https://botanical.com/botanical/mgmh/m/maples14.html" rel="noopener" target="_blank">https://botanical.com/botanical/mgmh/m/maples14.html</a>
 </p>
 <p>
  7. Native Languages of the Americas. (n.d.). <em>Native American Indian maple tree medicine, meaning and symbolism</em>. <a href="http://www.native-languages.org/legends-maple.htm" rel="noopener" target="_blank">http://www.native-languages.org/legends-maple.htm</a>
 </p>
 <p>
  8. Splitrock Environmental. (n.d.). <em>Douglas maple (sgw&aacute;lqwmaz&rsquo;)</em>. <a href="https://splitrockenvironmental.ca/products/douglas-maple-sgwalqwmaz" rel="noopener" target="_blank">https://splitrockenvironmental.ca/products/douglas-maple-sgwalqwmaz</a>
 </p>
 <p>
  9. Wikipedia contributors. (2024). <em>Acer glabrum</em>. In <em>Wikipedia</em>. <a href="https://en.wikipedia.org/wiki/Acer_glabrum" rel="noopener" target="_blank">https://en.wikipedia.org/wiki/Acer_glabrum</a>
 </p>
</section>"""

content = re.sub(r'<p>\s*1\) Elders.*?</section>', new_refs, content, flags=re.DOTALL)

with open('chapter_32.html', 'w', encoding='utf-8') as f:
    f.write(content)
