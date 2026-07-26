import re
import sys

def main():
    file_path = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters\chapter_24.html"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Image Labelling
    content = content.replace("Fig 24.1: [CAPTION_PLACEHOLDER]", "Fig 24.1: A blooming Canada Goldenrod (Solidago canadensis) plant showing its characteristic vibrant yellow flower clusters.")
    content = content.replace("Fig 24.2: [CAPTION_PLACEHOLDER]", "Fig 24.2: Close-up of a tall Solidago canadensis stalk with dense, yellow inflorescences.")
    content = content.replace("Fig 24.3: [CAPTION_PLACEHOLDER]", "Fig 24.3: Detailed view of the yellow flower heads of Canada Goldenrod.")
    content = content.replace("Fig 24.4: [CAPTION_PLACEHOLDER]", "Fig 24.4: Chemical structure of Rutin (Quercetin-3-O-rutinoside), a major flavonoid compound found in Solidago canadensis.")
    content = content.replace("Fig 24.5: [CAPTION_PLACEHOLDER]", "Fig 24.5: Chemical structure of a triterpenoid saponin (canadensissaponin) isolated from Solidago canadensis.")
    content = content.replace("Fig 24.6: [CAPTION_PLACEHOLDER]", "Fig 24.6: Detailed molecular structure of a complex bisdesmosidic saponin from Solidago canadensis.")

    # Fact Checking and Citations (Superscripting)
    content = content.replace("Canada Goldenrod, a native, long-lived perennial forms large, dense patches.", "Canada Goldenrod, a native, long-lived perennial forms large, dense patches<sup>[7]</sup>.")
    content = content.replace("Canada Goldenrod is named in honor of the many medicinal uses indigenous tribes found for the plant.", "Canada Goldenrod is named in honor of the many medicinal uses indigenous tribes found for the plant<sup>[5]</sup>.")
    content = content.replace("Its genus name “Solidago,” originates from the Latin word “solidare” which means “to make whole.”", "Its genus name “Solidago,” originates from the Latin word “solidare” which means “to make whole.”<sup>[8]</sup>")
    content = content.replace("and in burns and ulcer treatment. Indigenous peoples used", "and in burns and ulcer treatment<sup>[3]</sup>. Indigenous peoples used")
    content = content.replace("fevers, and inflammation. Some preparations", "fevers, and inflammation<sup>[7]</sup>. Some preparations")
    content = content.replace("for wounds and skin conditions.</p>", "for wounds and skin conditions.<sup>[7]</sup></p>")

    content = content.replace("flushing away infection and stones. The same tea", "flushing away infection and stones<sup>[5]</sup>. The same tea")
    content = content.replace("for those suffering from asthma or tuberculosis. When wounds,", "for those suffering from asthma or tuberculosis<sup>[11]</sup>. When wounds,")
    content = content.replace("known to be both astringent and healing.</p>", "known to be both astringent and healing.<sup>[10]</sup></p>")

    content = content.replace("ease arthritis, rheumatism, and swelling. The same", "ease arthritis, rheumatism, and swelling<sup>[12]</sup>. The same")
    content = content.replace("strength to the digestive system. Some used it", "strength to the digestive system<sup>[7]</sup>. Some used it")
    content = content.replace("health during menopause. Teas made from", "health during menopause<sup>[7]</sup>. Teas made from")
    content = content.replace("sore throats and mouth infections.</p>", "sore throats and mouth infections.<sup>[8]</sup></p>")

    content = content.replace("astragalin, and rutoside)</li>", "astragalin, and rutoside)<sup>[3]</sup></li>")
    
    content = content.replace("quercetin-3-O-beta-rutinoside (rutin)</li>", "quercetin-3-O-beta-rutinoside (rutin)<sup>[3]</sup></li>")
    content = content.replace("Isoquercitrin (Quercetin-3-O-β-glucoside)</li>", "Isoquercitrin (Quercetin-3-O-β-glucoside)<sup>[3]</sup></li>")
    content = content.replace("Astragalin (Kaempferol-3-O-β-glucoside)</li>", "Astragalin (Kaempferol-3-O-β-glucoside)<sup>[3]</sup></li>")
    content = content.replace("Hyperoside (Quercetin-3-O-β-galactoside)</li>", "Hyperoside (Quercetin-3-O-β-galactoside)<sup>[3]</sup></li>")

    content = content.replace("Antioxidant activity through hydrogen donation</p>", "Antioxidant activity through hydrogen donation<sup>[3]</sup></p>")
    content = content.replace("Anti-inflammatory via NF-κB pathway inhibition</p>", "Anti-inflammatory via NF-κB pathway inhibition<sup>[2]</sup></p>")
    content = content.replace("Capillary stabilization through collagen cross-linking</p>", "Capillary stabilization through collagen cross-linking<sup>[3]</sup></p>")

    content = content.replace("identified as bayogeninglycosides (canadensissaponins 1-4).</p>", "identified as bayogeninglycosides (canadensissaponins 1-4).<sup>[9]</sup></p>")
    
    content = content.replace("Complex bisdesmosidic structures</li>", "Complex bisdesmosidic structures<sup>[9]</sup></li>")
    content = content.replace("cause of vaginal and oral thrush</li>", "cause of vaginal and oral thrush<sup>[9]</sup></li>")
    content = content.replace("complexes with immune-stimulating properties</li>", "complexes with immune-stimulating properties<sup>[9]</sup></li>")

    content = content.replace("synaptic, and vanillin acids.</p>", "synaptic, and vanillin acids.<sup>[3]</sup></p>")
    content = content.replace("(834.50 ± 9.75 mg/g extract)</li>", "(834.50 ± 9.75 mg/g extract)<sup>[1]</sup></li>")
    content = content.replace("Neochlorogenic acid (5-O-caffeoylquinic acid)</li>", "Neochlorogenic acid (5-O-caffeoylquinic acid)<sup>[1]</sup></li>")
    content = content.replace("Caffeic acid derivatives</li>", "Caffeic acid derivatives<sup>[1]</sup></li>")

    content = content.replace("sabinene, and germacren D</p>", "sabinene, and germacren D<sup>[1]</sup></p>")
    content = content.replace("α-Pinene: Bronchodilator, antimicrobial</li>", "α-Pinene: Bronchodilator, antimicrobial<sup>[1]</sup></li>")
    content = content.replace("β-Pinene: Anti-inflammatory</li>", "β-Pinene: Anti-inflammatory<sup>[1]</sup></li>")
    content = content.replace("Germacrene D: Antimicrobial, insecticidal</li>", "Germacrene D: Antimicrobial, insecticidal<sup>[1]</sup></li>")
    content = content.replace("δ-Cadinene: Antimicrobial properties</li>", "δ-Cadinene: Antimicrobial properties<sup>[1]</sup></li>")

    content = content.replace("isolated from S. canadensis flowers.</p>", "isolated from S. canadensis flowers.<sup>[4]</sup></p>")

    content = content.replace("100% of furosemide at 20 mg/Kg b.wt.</p>", "100% of furosemide at 20 mg/Kg b.wt.<sup>[1]</sup></p>")
    
    content = content.replace("Increased glomerular filtration rate</li>", "Increased glomerular filtration rate<sup>[1]</sup></li>")
    content = content.replace("Enhanced sodium and chloride excretion</li>", "Enhanced sodium and chloride excretion<sup>[1]</sup></li>")
    content = content.replace("Vasodilation of renal blood vessels</li>", "Vasodilation of renal blood vessels<sup>[1]</sup></li>")
    content = content.replace("Inhibition of sodium reabsorption in distal tubules</li>", "Inhibition of sodium reabsorption in distal tubules<sup>[1]</sup></li>")

    content = content.replace("a large number of saponin molecules</p>", "a large number of saponin molecules<sup>[3]</sup></p>")
    content = content.replace("COX-2 inhibition by flavonoids</li>", "COX-2 inhibition by flavonoids<sup>[2]</sup></li>")
    content = content.replace("Lipoxygenase pathway suppression</li>", "Lipoxygenase pathway suppression<sup>[2]</sup></li>")
    content = content.replace("NF-κB transcription factor inhibition</li>", "NF-κB transcription factor inhibition<sup>[2]</sup></li>")
    content = content.replace("Cytokine production reduction</li>", "Cytokine production reduction<sup>[2]</sup></li>")

    content = content.replace("over S. virgaurea for gram-positive bacteria</li>", "over S. virgaurea for gram-positive bacteria<sup>[6]</sup></li>")
    content = content.replace("Cell membrane disruption by saponins</li>", "Cell membrane disruption by saponins<sup>[9]</sup></li>")
    content = content.replace("Protein synthesis inhibition</li>", "Protein synthesis inhibition<sup>[6]</sup></li>")
    content = content.replace("DNA replication interference</li>", "DNA replication interference<sup>[6]</sup></li>")
    content = content.replace("Biofilm formation prevention</li>", "Biofilm formation prevention<sup>[6]</sup></li>")

    content = content.replace("(Stable resonance structure prevents chain propagation)</p>", "(Stable resonance structure prevents chain propagation)<sup>[3]</sup></p>")
    content = content.replace("(DPPH radical scavenging assay principle)</p>", "(DPPH radical scavenging assay principle)<sup>[3]</sup></p>")
    content = content.replace("(Membrane destabilization leading to cell lysis)</p>", "(Membrane destabilization leading to cell lysis)<sup>[9]</sup></p>")
    content = content.replace("(Antifungal mechanism through membrane permeabilization)</p>", "(Antifungal mechanism through membrane permeabilization)<sup>[9]</sup></p>")
    content = content.replace("aquaretic activity of the different extracts and fractions</p>", "aquaretic activity of the different extracts and fractions<sup>[1]</sup></p>")
    content = content.replace("Phenolic Compounds + Renal Transporters → Modified Ion Transport</p>", "Phenolic Compounds + Renal Transporters → Modified Ion Transport<sup>[1]</sup></p>")
    content = content.replace("Flavonoids + Aquaporin Channels → Enhanced Water Excretion</p>", "Flavonoids + Aquaporin Channels → Enhanced Water Excretion<sup>[1]</sup></p>")

    content = content.replace("and 39.75 ± 0.005 g RE/100 g dried extract, respectively)</p>", "and 39.75 ± 0.005 g RE/100 g dried extract, respectively)<sup>[1]</sup></p>")
    content = content.replace("apiofuranoside (7) from genus Solidago</p>", "apiofuranoside (7) from genus Solidago<sup>[1]</sup></p>")
    content = content.replace("inflammatory diseases of the urinary tract</p>", "inflammatory diseases of the urinary tract<sup>[8]</sup></p>")

    content = content.replace("Safety in pregnancy is unknown</p>", "Safety in pregnancy is unknown<sup>[8]</sup></p>")
    content = content.replace("In other words, drink your tea!</p>", "In other words, drink your tea!<sup>[3]</sup></p>")
    content = content.replace("water was the best solvent for the extraction of its saponins</p>", "water was the best solvent for the extraction of its saponins<sup>[1]</sup></p>")

    # Replace references section
    old_refs_start = content.find('<p>\n  1) Elders')
    if old_refs_start == -1:
        old_refs_start = content.find('<p>\n   1) Elders')
    if old_refs_start == -1:
        old_refs_start = content.find('<p>1) Elders')
    # Use regex to find start of first reference
    import re
    match = re.search(r'<p>\s*1\)\s*Elders', content)
    if match:
        old_refs_start = match.start()
        
    old_refs_end = content.find('</section>')

    new_references_html = """<p>1. Abdel Baki, P. M., El-Sherei, M. M., Khaleel, A. E., Abdel Motaal, A. A., &amp; Ibrahim Abdallah, H. M. (2019). Aquaretic activity of <em>Solidago canadensis</em> cultivated in Egypt and determination of the most bioactive fraction. <em>Iranian Journal of Pharmaceutical Research, 18</em>(2), 922–937. <a href="https://doi.org/10.22037/ijpr.2019.2390">https://doi.org/10.22037/ijpr.2019.2390</a></p>
 <p>2. Apáti, P., Houghton, P. J., Kite, G., Steventon, G. B., &amp; Kéry, Á. (2006). In-vitro effect of flavonoids from <em>Solidago canadensis</em> extract on glutathione S-transferase. <em>Journal of Pharmacy and Pharmacology, 58</em>(2), 251–256. <a href="https://doi.org/10.1211/jpp.58.2.0013">https://doi.org/10.1211/jpp.58.2.0013</a></p>
 <p>3. Apáti, P., Szentmihályi, K., Kristó, T. S., Papp, I., Vinkler, P., Szőke, É., &amp; Kéry, Á. (2003). Herbal remedies of <em>Solidago</em>—Correlation of phytochemical characteristics and antioxidative properties. <em>Journal of Pharmaceutical and Biomedical Analysis, 32</em>(4–5), 1045–1053. <a href="https://doi.org/10.1016/S0731-7085(03)00207-3">https://doi.org/10.1016/S0731-7085(03)00207-3</a></p>
 <p>4. Bradette-Hébert, M.-E., Legault, J., Lavoie, S., &amp; Pichette, A. (2008). A new labdane diterpene from the flowers of <em>Solidago canadensis</em>. <em>Chemical and Pharmaceutical Bulletin, 56</em>(1), 82–84. <a href="https://doi.org/10.1248/cpb.56.82">https://doi.org/10.1248/cpb.56.82</a></p>
 <p>5. Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.). <em>Traditional knowledge of Canada Goldenrod</em>.</p>
 <p>6. Kołodziej, B., Kowalski, R., &amp; Kędzia, B. (2011). Antibacterial and antimutagenic activity of extracts of above-ground parts of three <em>Solidago</em> species. <em>Journal of Medicinal Plants Research, 5</em>(31), 6770–6779. <a href="https://doi.org/10.5897/JMPR11.1098">https://doi.org/10.5897/JMPR11.1098</a></p>
 <p>7. Moerman, D. E. (1998). <em>Native American ethnobotany</em>. Timber Press.</p>
 <p>8. Mount Sinai Health System. (n.d.). <em>Goldenrod</em>. Mount Sinai Health Library. https://www.mountsinai.org/health-library/herb/goldenrod</p>
 <p>9. Reznicek, G., Jurenitsch, J., Plasun, M., Korhammer, S., Haslinger, E., Hiller, K., &amp; Kubelka, W. (1991). Four major saponins from <em>Solidago canadensis</em>. <em>Phytochemistry, 30</em>(5), 1629–1633. <a href="https://doi.org/10.1016/0031-9422(91)84222-E">https://doi.org/10.1016/0031-9422(91)84222-E</a></p>
 <p>10. Rousseau, J. (1945). Études ethnobotaniques québécoises: Le folklore botanique de Caughnawaga. <em>Contributions de l’Institut botanique de l’Université de Montréal, 55</em>, 7–72. <a href="https://www2.ville.montreal.qc.ca/jardin/archives/rousseau/publi/Etudes_ethnobotaniques_quebecoises.pdf">https://www2.ville.montreal.qc.ca/jardin/archives/rousseau/publi/Etudes_ethnobotaniques_quebecoises.pdf</a></p>
 <p>11. Smith, H. H. (1933). <em>Ethnobotany of the Forest Potawatomi Indians</em> (Bulletin of the Public Museum of the City of Milwaukee, Vol. 7, No. 1). Milwaukee Public Museum.</p>
 <p>12. Turner, N. J., Bouchard, R., &amp; Kennedy, D. I. D. (1980). <em>Ethnobotany of the Okanagan-Colville Indians of British Columbia and Washington</em> (Occasional Paper No. 21). British Columbia Provincial Museum.</p>
"""

    if match:
        content = content[:old_refs_start] + new_references_html + content[old_refs_end:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success")

if __name__ == "__main__":
    main()
