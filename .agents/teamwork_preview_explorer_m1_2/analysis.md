# Chapter 8-14 Reference Exploration & Audit Analysis

## Executive Summary

This report presents the complete reference investigation and audit for **Milestone 1 (Chapters 8 through 14)** of the *Indigenous Medicines / Bold Hawking* project.

Across Chapters 8 through 14, a total of **71 reference items** were extracted and analyzed. The investigation revealed major HTML structural inconsistencies, widespread malformed anchor tags (nested `<a>` tags and broken `href` attributes), missing reference sections, non-standard `<p>` lists, and significant missing or broken DOI links.

### Key Metrics Overview Table

| Metric | Count | Percentage | Description |
|---|---|---|---|
| **Total Chapters Audited** | 7 | 100% | `chapter_08.html` to `chapter_14.html` |
| **Total Reference Items** | 71 | 100% | Total extracted citation items |
| **Valid & Verified DOIs** | 29 | 40.8% | DOIs present, resolving HTTP 200, matching paper title |
| **Hallucinated DOIs** | 4 | 5.6% | DOIs present but pointing to unrelated papers |
| **Broken HTTP / Non-functional DOIs** | 3 | 4.2% | DOIs present returning 404 or HTTP errors |
| **Missing DOIs/URLs** | 35 | 49.3% | Reference items with no DOI or anchor tag |
| **Malformed HTML Anchor Tags** | 4 | 5.6% | Items with nested `<a>` tags, unclosed tags, or malformed attributes |

## Chapter-by-Chapter Inventory & Structural Analysis

| Chapter File | References Heading | HTML Container | Ref Count | Valid DOI | Hallucinated | Broken HTTP | Missing DOI | Malformed HTML |
|---|---|---|---|---|---|---|---|---|
| `chapter_08.html` | `Yes` | `<ol>` | 16 | 10 | 0 | 0 | 6 | 1 |
| `chapter_09.html` | `Yes` | `NO_REF_LIST_FOUND` | 0 | 0 | 0 | 0 | 0 | 0 |
| `chapter_10.html` | `Yes` | `<ol>` | 6 | 2 | 0 | 0 | 4 | 0 |
| `chapter_11.html` | `Yes` | `<p> list` | 23 | 8 | 3 | 2 | 10 | 1 |
| `chapter_12.html` | `Yes` | `<ol>` | 11 | 5 | 1 | 0 | 5 | 1 |
| `chapter_13.html` | `Yes` | `<ol>` | 6 | 0 | 0 | 1 | 5 | 1 |
| `chapter_14.html` | `Yes` | `<ol>` | 9 | 4 | 0 | 0 | 5 | 0 |


## Deep Dive Structural Findings

### 1. Missing Reference List in Chapter 9 (`chapter_09.html`)
- **Finding**: `chapter_09.html` (Mullein Leaf Tea) contains a `References` heading (`<p><span style="color: #339966"><strong>References</strong></span></p>`), but **NO reference list (<ol> or <p>) exists beneath it**.
- **Impact**: In-text citations in Chapter 9 (e.g., `[4]`, `[9]`, `[10]`, `[12]`, `[15]`, `[17]`) cannot be resolved against any reference list in the chapter HTML file.
- **Action Required**: Reconstruct/restore the 17 missing reference items for Chapter 9 from source manuscript or CrossRef search.

### 2. Non-Standard `<p>` List Tagging in Chapter 11 (`chapter_11.html`)
- **Finding**: `chapter_11.html` (Sage Tea) lists 23 references under `<p><strong><span style="color: #339966">References</span></strong></p>`, but **uses individual `<p>` paragraphs** (`<p>1. Adams...</p>`, `<p>2. Anibogwu...</p>`) instead of a semantic `<ol><li>` list.
- **Impact**: Standard BeautifulSoup extraction scripts expecting `<ol><li>` fail to parse Chapter 11 references.
- **Action Required**: Convert all 23 reference `<p>` tags in `chapter_11.html` into a clean `<ol><li>` ordered list structure.

### 3. Widespread Malformed HTML Anchor Tags & Nested `<a>` Tags
- **Nested `<a>` Tags**: Chapters 8, 10, 12, 13, 14 contain nested anchor tags created by automated string replacement or bad conversion: `<a href="https://doi.org/..."><a href="https://doi.org/...">https://doi.org/...</a></a>`.
- **Truncated and Malformed `href` Attributes**: In multiple chapters (e.g., `chapter_08.html` line 740, `chapter_11.html` line 55, `chapter_12.html` line 384, `chapter_13.html` line 208), Splitrock Environmental URLs contain broken attributes like `<a href="&lt;a href=" https:="" splitrockenvironmental.ca"="">
- **Split Image Source Links**: In `chapter_12.html` (lines 84-89, 124-129), ResearchGate URLs in figure captions were broken into two separate `<a href="...">` tags split across line breaks.

## Complete Reference Inventory (Chapters 8-14)

### chapter_08.html (16 References)

#### Reference 8.html.1
- **Reference Text**: Bocek, B. R. (1984). Ethnobotany of Costanoan Indians, California, based on collections by John P. Harrington.Economic Botany,38(2), 240–255.https://doi.org/10.1007/BF02858839
- **DOI Status**: `OK`
- **Existing DOI**: `10.1007/BF02858839`

#### Reference 8.html.2
- **Reference Text**: Cayoose Creek Band of Sekw’el’was Elders and Community members. (n.d.).Traditional knowledge.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference

#### Reference 8.html.3
- **Reference Text**: Filipowicz, N., Kamiński, M., Kurlenda, J., Asztemborska, M., & Ochocka, J. R. (2003). Antibacterial and antifungal activity of juniper berry oil and its selected components.Phytotherapy Research,17(3), 227–231.https://doi.org/10.1002/ptr.1110
- **DOI Status**: `OK`
- **Existing DOI**: `10.1002/ptr.1110`

#### Reference 8.html.4
- **Reference Text**: Glišić, S. B., Milojević, S. Ž., Dimitrijević, S. I., Orlović, A. M., & Skala, D. U. (2007). Antimicrobial activity of the essential oil and different fractions ofJuniperus communisL. and a comparison with some commercial antibiotics.Journal of the Serbian Chemical Society,72(4), 311–320.https://doi.org/10.2298/JSC0704311G
- **DOI Status**: `OK`
- **Existing DOI**: `10.2298/JSC0704311G`

#### Reference 8.html.5
- **Reference Text**: Gonçalves, A. C., Flores-Félix, J. D., Coutinho, P., Alves, G., & Silva, L. R. (2022). Zimbro (Juniperus communisL.) as a promising source of bioactive compounds and biomedical activities: A review on recent trends.International Journal of Molecular Sciences,23(6), 3197.https://doi.org/10.3390/ijms23063197
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/ijms23063197`

#### Reference 8.html.6
- **Reference Text**: Höferl, M., Stoilova, I., Schmidt, E., Wanner, J., Jirovetz, L., Trifonova, D., Krastev, L., & Krastanov, A. (2014). Chemical composition and antioxidant properties of juniper berry (Juniperus communisL.) essential oil: Action of the essential oil on the antioxidant protection ofSaccharomyces cerevisiaemodel organism.Antioxidants,3(1), 81–98.https://doi.org/10.3390/antiox3010081
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/antiox3010081`

#### Reference 8.html.7
- **Reference Text**: Jones, B. (2024).Medicinal herbs of Western Canada: A pictorial manual(1st ed.). Nimbus Publishing.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.21825/af.v10i3-4.17689`

#### Reference 8.html.8
- **Reference Text**: Mascolo, N., Autore, G., Capasso, F., Menghini, A., & Fasulo, M. P. (1987). Biological screening of Italian medicinal plants for anti-inflammatory activity.Phytotherapy Research,1(1), 28–31.https://doi.org/10.1002/ptr.2650010107
- **DOI Status**: `OK`
- **Existing DOI**: `10.1002/ptr.2650010107`

#### Reference 8.html.9
- **Reference Text**: Miyazawa, M., & Yamafuji, C. (2005). Inhibition of acetylcholinesterase activity by bicyclic monoterpenoids.Journal of Agricultural and Food Chemistry,53(5), 1765–1768.https://doi.org/10.1021/jf040019b
- **DOI Status**: `OK`
- **Existing DOI**: `10.1021/jf040019b`

#### Reference 8.html.10
- **Reference Text**: Moerman, D. E. (1998).Native American ethnobotany. Timber Press.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/1224232`

#### Reference 8.html.11
- **Reference Text**: Pepeljnjak, S., Kosalec, I., Kalodera, Z., & Blažević, N. (2005). Antimicrobial activity of juniper berry essential oil (Juniperus communisL., Cupressaceae).Acta Pharmaceutica,55(4), 417–422.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.3403/30180606`

#### Reference 8.html.12
- **Reference Text**: Raina, R., Verma, P. K., Peshin, R., & Kour, H. (2019). Potential ofJuniperus communisL as a nutraceutical in human and veterinary medicine.Heliyon,5(8), e02376.https://doi.org/10.1016/j.heliyon.2019.e02376
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/j.heliyon.2019.e02376`

#### Reference 8.html.13
- **Reference Text**: Sánchez de Medina, F., Gámez, M. J., Jiménez, I., Jiménez, J., Osuna, J. I., & Zarzuelo, A. (1994). Hypoglycemic activity of juniper “berries.”Planta Medica,60(3), 197–200.https://doi.org/10.1055/s-2006-959457
- **DOI Status**: `OK`
- **Existing DOI**: `10.1055/s-2006-959457`

#### Reference 8.html.14
- **Reference Text**: Splitrock Environmental. (n.d.).Common Juniper (tsíktsektaz’). Retrieved November 7, 2024, fromhttps://splitrockenvironmental.ca/products/common-juniper-tsiktsektaz?variant=40347042218150">https://splitrockenvironmental.ca/products/common-juniper-tsiktsektaz?variant=40347042218150
- **DOI Status**: `MISSING`
- **Formatting Issues**: Malformed href attribute containing embedded <a> tag
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1079/cabicompendium.29085`

#### Reference 8.html.15
- **Reference Text**: Swanston-Flatt, S. K., Day, C., Bailey, C. J., & Flatt, P. R. (1990). Traditional plant treatments for diabetes: Studies in normal and streptozotocin diabetic mice.Diabetologia,33(8), 462–464.https://doi.org/10.1007/BF00405106
- **DOI Status**: `OK`
- **Existing DOI**: `10.1007/BF00405106`

#### Reference 8.html.16
- **Reference Text**: Tilford, G. L. (1997).Edible and medicinal plants of the West. Mountain Press Publishing Company.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/1222475`

### chapter_09.html (0 References)

*No reference list present in HTML file.*

### chapter_10.html (6 References)

#### Reference 10.html.1
- **Reference Text**: Deane, G. (n.d.).Rose hips. Eat The Weeds.https://www.eattheweeds.com/rose-hips/
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1016/s0140-6736(45)91770-3`

#### Reference 10.html.2
- **Reference Text**: Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.).Traditional knowledge and uses of plants.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.56042/ijtk.v25i4.22880`

#### Reference 10.html.3
- **Reference Text**: Joseph, L. (n.d.).Recipe: Rosehip, nettle and mint tea for boosting immunity. Skwálwen.https://skwalwen.com/blogs/news/recipe-rosehip-nettle-and-mint-tea-for-boosting-immunity
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/j.ctv2057qq4.22`

#### Reference 10.html.4
- **Reference Text**: Mármol, I., Sánchez-de-Diego, C., Jiménez-Moreno, N., Ancín-Azpilicueta, C., & Rodríguez-Yoldi, M. J. (2017). Therapeutic applications of rose hips from differentRosaspecies.International Journal of Molecular Sciences,18(6), 1137.https://doi.org/10.3390/ijms18061137
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/ijms18061137`

#### Reference 10.html.5
- **Reference Text**: Splitrock Environmental. (n.d.).Prairie rose (qel’q).https://splitrockenvironmental.ca/products/prairie-rose-qel-q?variant=40368083304614
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference

#### Reference 10.html.6
- **Reference Text**: Winther, K., Vinther Hansen, A. S., & Campbell-Tofte, J. (2015). Bioactive ingredients of rose hips (Rosa caninaL) with special reference to antioxidative and anti-inflammatory properties: In vitro studies.Botanics: Targets and Therapy,5, 11–23.https://doi.org/10.2147/BTAT.S91385
- **DOI Status**: `OK`
- **Existing DOI**: `10.2147/BTAT.S91385`

### chapter_11.html (23 References)

#### Reference 11.html.1
- **Reference Text**: 1. Adams, J. D., & Garcia, C. (2005). The advantages of traditional Chumash healing.Evidence-Based Complementary and Alternative Medicine,2(1), 19–23.https://doi.org/10.1093/ecam/neh050
- **DOI Status**: `HALLUCINATED`
- **Existing DOI**: `10.1093/ecam/neh050`
- **DOI Issues**: HALLUCINATED DOI: 10.1093/ecam/neh050 resolves to 'Education in Oriental Medicine in Kyung Hee University', which does NOT match reference text '1. Adams, J. D., & Garcia, C. (2005). The advantages of traditional Chumash healing.Evidence-Based C...'
- **Suggested DOI**: `https://doi.org/10.1093/ecam/neh072`

#### Reference 11.html.2
- **Reference Text**: 2. Anibogwu, R., De Jesus, K., Pradhan, S., Van Leuven, S., & Sharma, K. (2024). Sesquiterpene lactones and flavonoid from the leaves of basin big sagebrush (Artemisia tridentatasubsp.tridentata): Isolation, characterization and biological activities.Molecules,29(4), 802.https://doi.org/10.3390/molecules29040802
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/molecules29040802`

#### Reference 11.html.3
- **Reference Text**: 3. Asikinak, B. (n.d.). Smudging. InIndigenous Saskatchewan Encyclopedia. Retrieved April 18, 2025, fromhttps://teaching.usask.ca/indigenoussk/import/smudging.php
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference

#### Reference 11.html.4
- **Reference Text**: 4. Baricevic, D., & Bartol, T. (2000). The biological/pharmacological activity of theSalviagenus. In S. E. Kintzios (Ed.),Sage: The genus Salvia(pp. 143–184). Harwood Academic Publishers.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.4324/9780203168875.ch8`

#### Reference 11.html.5
- **Reference Text**: 5. Barrows, D. P. (1977).Ethno-botany of the Coahuilla Indians of Southern California(Reprint of 1900 ed.). Malki Museum Press.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.5962/bhl.title.19178`

#### Reference 11.html.6
- **Reference Text**: 6. Bean, L. J., & Saubel, K. S. (1972).Temalpakh: Cahuilla Indian knowledge and usage of plants. Malki Museum Press.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/25157458`

#### Reference 11.html.7
- **Reference Text**: 7. California Native Plant Society. (n.d.).Saging the world. Retrieved April 18, 2025, fromhttps://www.cnps.org/conservation/white-sage
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1525/9780520353091-003`

#### Reference 11.html.8
- **Reference Text**: 8. Elders and community members of the Cayoose Creek Band of Sekw’el’was. (n.d.).
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.31390/gradschool_dissertations.340`

#### Reference 11.html.9
- **Reference Text**: 9. Ghorbani, A., & Esmaeilizadeh, M. (2017). Pharmacological properties ofSalvia officinalisand its components.Journal of Traditional and Complementary Medicine,7(4), 433–440.https://doi.org/10.1016/j.jtcme.2016.12.014
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/j.jtcme.2016.12.014`

#### Reference 11.html.10
- **Reference Text**: 10. Hamidpour, M., Hamidpour, R., Hamidpour, S., & Shahlari, M. (2014). Chemistry, pharmacology, and medicinal property of sage (Salvia) to prevent and cure illnesses such as obesity, diabetes, depression, dementia, lupus, autism, heart disease, and cancer.Journal of Traditional and Complementary Medicine,4(2), 82–88.https://doi.org/10.4103/2225-4110.130373
- **DOI Status**: `OK`
- **Existing DOI**: `10.4103/2225-4110.130373`

#### Reference 11.html.11
- **Reference Text**: 11. Jones, R. (2024).Medicinal herbs of Western Canada(1st ed.). Nimbus Publishing.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.21825/af.v10i3-4.17689`

#### Reference 11.html.12
- **Reference Text**: 12. Lopresti, A. L. (2017).Salvia(sage): A review of its potential cognitive-enhancing and protective effects.Drugs in R&D,17(1), 53–64.https://doi.org/10.1007/s40268-016-0157-8
- **DOI Status**: `BROKEN_HTTP`
- **Existing DOI**: `10.1007/s40268-016-0157-8`
- **DOI Issues**: Existing DOI (10.1007/s40268-016-0157-8) returned HTTP 404
- **Suggested DOI**: `https://doi.org/10.1007/s40268-016-0157-5`

#### Reference 11.html.13
- **Reference Text**: 13. Moerman, D. E. (1998).Native American ethnobotany. Timber Press.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/1224232`

#### Reference 11.html.14
- **Reference Text**: 14. Nigam, M., Atanassova, M., Mishra, A. P., Pezzani, R., Devkota, H. P., Plygun, S., Salehi, B., Setzer, W. N., & Sharifi-Rad, J. (2019). Bioactive compounds and health benefits ofArtemisiaspecies.Natural Product Communications,14(7).https://doi.org/10.1177/1934578X19850354
- **DOI Status**: `OK`
- **Existing DOI**: `10.1177/1934578X19850354`

#### Reference 11.html.15
- **Reference Text**: 15. Perry, N. S., Bollen, C., Perry, E. K., & Ballard, C. (2003).Salviafor dementia therapy: Review of pharmacological activity and pilot tolerability clinical trial.Pharmacology Biochemistry and Behavior,75(3), 651–659.https://doi.org/10.1016/S0091-3057(03)00108-4
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/S0091-3057(03)00108-4`

#### Reference 11.html.16
- **Reference Text**: 16. Raman, R. (2023).9 emerging benefits and uses of sage tea. Healthline.https://www.healthline.com/nutrition/sage-tea
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1080/87559129509541057`

#### Reference 11.html.17
- **Reference Text**: 17. Ramos, A. A., Azqueta, A., Pereira-Wilson, C., & Collins, A. R. (2010). Polyphenolic compounds fromSalviaspecies protect cellular DNA from oxidation and stimulate DNA repair in cultured human cells.Journal of Agricultural and Food Chemistry,58(12), 7465–7471.https://doi.org/10.1021/jf100871b
- **DOI Status**: `BROKEN_HTTP`
- **Existing DOI**: `10.1021/jf100871b`
- **DOI Issues**: Existing DOI (10.1021/jf100871b) returned HTTP 404
- **Suggested DOI**: `https://doi.org/10.1021/jf100082p`

#### Reference 11.html.18
- **Reference Text**: 18. Sa, C. M., Ramos, A. A., Azevedo, M. F., Lima, C. F., Fernandes-Ferreira, M., & Pereira-Wilson, C. (2009). Sage tea drinking improves lipid profile and antioxidant defences in humans.International Journal of Molecular Sciences,10(9), 3937–3950.https://doi.org/10.3390/ijms10093937
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/ijms10093937`

#### Reference 11.html.19
- **Reference Text**: 19. Schaffer, S., Müller, W. E., & Eckert, G. P. (2013). Tocopherols, tocotrienols, and brain health. In A. M. Schaffer, W. E. Müller, & G. P. Eckert (Eds.),Aging and health – A systems biology perspective(Vol. 40, pp. 121–131). Karger Publishers.https://doi.org/10.1159/000346229
- **DOI Status**: `HALLUCINATED`
- **Existing DOI**: `10.1159/000346229`
- **DOI Issues**: HALLUCINATED DOI: 10.1159/000346229 resolves to 'Patterns of Subarachnoid Hemorrhage Admissions in England, 2008–2011', which does NOT match reference text '19. Schaffer, S., Müller, W. E., & Eckert, G. P. (2013). Tocopherols, tocotrienols, and brain health...'
- **Suggested DOI**: `https://doi.org/10.1093/jn/135.2.151`

#### Reference 11.html.20
- **Reference Text**: 20. Splitrock Environmental. (n.d.).Sage (káwkwu). Retrieved November 19, 2024, fromhttps://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294">https://splitrockenvironmental.ca/products/big-sagebrush-kawkwu?variant=40347062960294
- **DOI Status**: `MISSING`
- **Formatting Issues**: Malformed href attribute containing embedded <a> tag
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1385/0-89603-566-2:109`

#### Reference 11.html.21
- **Reference Text**: 21. Tildesley, N. T., Kennedy, D. O., Perry, E. K., Ballard, C. G., Savelev, S., Wesnes, K. A., & Scholey, A. B. (2003).Salvia lavandulaefolia(Spanish sage) enhances memory in healthy young volunteers.Pharmacology Biochemistry and Behavior,75(3), 669–674.https://doi.org/10.1016/S0091-3057(03)00122-9
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/S0091-3057(03)00122-9`

#### Reference 11.html.22
- **Reference Text**: 22. Timbrook, J. (1990). Ethnobotany of Chumash Indians, California, based on collections by John P. Harrington.Economic Botany,44(2), 236–253.https://doi.org/10.1007/BF02860478
- **DOI Status**: `HALLUCINATED`
- **Existing DOI**: `10.1007/BF02860478`
- **DOI Issues**: HALLUCINATED DOI: 10.1007/BF02860478 resolves to 'Quinua and Relatives (Chenopodium sect.Chenopodium subsect.Celluloid)', which does NOT match reference text '22. Timbrook, J. (1990). Ethnobotany of Chumash Indians, California, based on collections by John P....'
- **Suggested DOI**: `https://doi.org/10.1007/bf02860489`

#### Reference 11.html.23
- **Reference Text**: 23. Wightman, E. L., Jackson, P. A., Spittlehouse, B., Heffernan, T., Guillemet, D., & Kennedy, D. O. (2021). The acute and chronic cognitive effects of a sage extract: A randomized, placebo-controlled study in healthy humans.Nutrients,13(1), 218.https://doi.org/10.3390/nu13010218
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/nu13010218`

### chapter_12.html (11 References)

#### Reference 12.html.1
- **Reference Text**: Brunning, A. (2015).The chemistry of stinging nettles. Compound Interest.https://www.compoundchem.com/2015/06/04/nettles/
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1021/cen-09315-scitech2`

#### Reference 12.html.2
- **Reference Text**: Chrubasik, J. E., Roufogalis, B. D., Wagner, H., & Chrubasik, S. (2007). A comprehensive review on the stinging nettle effect and efficacy profiles. Part II:Urticae radix.Phytomedicine, 14(7–8), 568–579.https://doi.org/10.1016/j.phymed.2007.03.014
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/j.phymed.2007.03.014`

#### Reference 12.html.3
- **Reference Text**: Durovic, S., Kojic, I., Radic, D., Smyatskaya, Y. A., Bazarnova, J. G., Filip, S., & Tosti, T. (2024). Chemical constituent of stinging nettle (Urtica dioicaL.): A comprehensive review on phenolic and polyphenolic compounds and their bioactivity.International Journal of Molecular Sciences, 25(6), 3430.https://doi.org/10.3390/ijms25063430
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/ijms25063430`

#### Reference 12.html.4
- **Reference Text**: Elders and Community Members of the Cayoose Creek Band of Sekw’el’was. (n.d.).
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.31390/gradschool_dissertations.340`

#### Reference 12.html.5
- **Reference Text**: Gülçin, İ., Küfrevioğlu, Ö. İ., Oktay, M., & Büyükokuroğlu, M. E. (2004). Antioxidant, antimicrobial, antiulcer and analgesic activities of nettle (Urtica dioica).Journal of Ethnopharmacology, 90(2–3), 205–215.https://doi.org/10.1016/j.jep.2003.09.028
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/j.jep.2003.09.028`

#### Reference 12.html.6
- **Reference Text**: Hamel, P. B., & Chiltoskey, M. U. (1975).Cherokee plants and their uses: A 400 year history. Herald Publishing Co.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference

#### Reference 12.html.7
- **Reference Text**: Jones, B. (2024).Medicinal herbs of Western Canada(1st ed.). Nimbus Publishing.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.21825/af.v10i3-4.17689`

#### Reference 12.html.8
- **Reference Text**: Konrad, L., Müller, H. H., Lenz, C., Laubinger, H., Aumüller, G., & Lichius, J. J. (2000). Antiproliferative effect on human prostate cancer cells by a stinging nettle root (Urtica dioica) extract.Planta Medica, 66(1), 44–47.https://doi.org/10.1055/s-2000-11120
- **DOI Status**: `HALLUCINATED`
- **Existing DOI**: `10.1055/s-2000-11120`
- **DOI Issues**: HALLUCINATED DOI: 10.1055/s-2000-11120 resolves to 'Steroids from Harrisonia abyssinica', which does NOT match reference text 'Konrad, L., Müller, H. H., Lenz, C., Laubinger, H., Aumüller, G., & Lichius, J. J. (2000). Antiproli...'
- **Suggested DOI**: `https://doi.org/10.1055/s-2000-11117`

#### Reference 12.html.9
- **Reference Text**: Kregiel, D., Pawlikowska, E., & Antolak, H. (2018).Urticaspp.: Ordinary plants with extraordinary properties.Molecules, 23(7), 1664.https://doi.org/10.3390/molecules23071664
- **DOI Status**: `OK`
- **Existing DOI**: `10.3390/molecules23071664`

#### Reference 12.html.10
- **Reference Text**: Mittman, P. (1990). Randomized, double-blind study of freeze-driedUrtica dioicain the treatment of allergic rhinitis.Planta Medica, 56(1), 44–47.https://doi.org/10.1055/s-2006-960881
- **DOI Status**: `OK`
- **Existing DOI**: `10.1055/s-2006-960881`

#### Reference 12.html.11
- **Reference Text**: Splitrock Environmental. (n.d.).Stinging nettle salve.https://splitrockenvironmental.ca/products/stinging-nettle-salve?variant=33785190744123">https://splitrockenvironmental.ca/products/stinging-nettle-salve?variant=33785190744123
- **DOI Status**: `MISSING`
- **Formatting Issues**: Malformed href attribute containing embedded <a> tag
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.31003/uspnf_m56480_02_01`

### chapter_13.html (6 References)

#### Reference 13.html.1
- **Reference Text**: Abdulladjanova, N. G., Mavlonov, G. T., Mamadrahimov, A. A., Rakhimov, R. N., Ning, H., Wali, A., Yili, A., & Abdulla, R. (n.d.).Phenolic compounds of Rhus glabra.https://www.jrespharm.com/uploads/pdf/pdf_MPJ_1485.pdf
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.29228/jrp.607`

#### Reference 13.html.2
- **Reference Text**: Lord, A. (2019, July 2).Beware poison sumac (Rhus vernix). UNH Extension.https://extension.unh.edu/blog/2019/07/beware-poison-sumac-rhus-vernix
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/jj.30347469.26`

#### Reference 13.html.3
- **Reference Text**: National Center for Biotechnology Information. (2025).PubChem compound summary for CID 1183, vanillin.https://pubchem.ncbi.nlm.nih.gov/compound/Vanillin
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.7717/peerj.14915/fig-2`

#### Reference 13.html.4
- **Reference Text**: Opiyo, S. A., Njoroge, P. W., Ndirangu, E. G., & Kuria, K. M. (2021). A review of biological activities and phytochemistry of Rhus species.American Journal of Chemistry,11(2).https://doi.org/10.5923/j.chemistry.20211102.02
- **DOI Status**: `BROKEN_HTTP`
- **Existing DOI**: `10.5923/j.chemistry.20211102.02`
- **DOI Issues**: Existing DOI (10.5923/j.chemistry.20211102.02) returned HTTP 404
- **Suggested DOI**: `https://doi.org/10.1016/j.phytochem.2020.112540`

#### Reference 13.html.5
- **Reference Text**: Splitrock Environmental. (2025).Smooth sumac (nekw’tsamúm’l).https://splitrockenvironmental.ca/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518">https://splitrockenvironmental.ca/collections/plants/products/smooth-sumac-nekw-tsamum-l?variant=40347085668518
- **DOI Status**: `MISSING`
- **Formatting Issues**: Malformed href attribute containing embedded <a> tag
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.1079/cabicompendium.47398`

#### Reference 13.html.6
- **Reference Text**: United States Department of Agriculture Natural Resources Conservation Service. (2004).Plant guide for smooth sumac (Rhus glabra L.).https://plants.usda.gov/DocumentLibrary/plantguide/pdf/cs_rhgl.pdf
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference

### chapter_14.html (9 References)

#### Reference 14.html.1
- **Reference Text**: Ali, S. I., Gopalakrishnan, B., & Venkatesalu, V. (2017). Pharmacognosy, phytochemistry and pharmacological properties ofAchillea millefolium: A review.Phytotherapy Research, 31(8), 1140–1161.https://doi.org/10.1002/ptr.5840
- **DOI Status**: `OK`
- **Existing DOI**: `10.1002/ptr.5840`

#### Reference 14.html.2
- **Reference Text**: Applequist, W. L., & Moerman, D. E. (2011). Yarrow (Achillea millefolium): A neglected panacea? A review of ethnobotany, bioactivity, and biomedical research.Economic Botany, 65(2), 209–225.https://doi.org/10.1007/s12231-011-9154-3
- **DOI Status**: `OK`
- **Existing DOI**: `10.1007/s12231-011-9154-3`

#### Reference 14.html.3
- **Reference Text**: Elders and Community Members of the Cayoose Creek Band of Sekw’el’was. (n.d.). [Traditional knowledge and personal communications].
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.31390/gradschool_dissertations.340`

#### Reference 14.html.4
- **Reference Text**: European Medicines Agency. (2019).European Union herbal monograph on Achillea millefolium, herba(Revision 1) [Draft]. Committee on Herbal Medicinal Products.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.32782/2522-9680-2025-3-167`

#### Reference 14.html.5
- **Reference Text**: Jones, R. (2024).Medicinal herbs of Western Canada(1st ed.). Nimbus Publishing.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.21825/af.v10i3-4.17689`

#### Reference 14.html.6
- **Reference Text**: Kazemi, M. (2015). Chemical composition and antimicrobial, antioxidant activities and anti-inflammatory potential ofAchillea millefolium,Anethum graveolensL., andCarum copticumL. essential oils.Journal of Herbal Medicine, 5(4), 217–222.https://doi.org/10.1016/j.hermed.2015.09.001
- **DOI Status**: `OK`
- **Existing DOI**: `10.1016/j.hermed.2015.09.001`

#### Reference 14.html.7
- **Reference Text**: Moerman, D. E. (1998).Native American ethnobotany. Timber Press.
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference
- **Suggested DOI**: `https://doi.org/10.2307/1224232`

#### Reference 14.html.8
- **Reference Text**: Saeidnia, S., Gohari, A. R., Mokhber-Dezfuli, N., & Kiuchi, F. (2011). A review on phytochemistry and medicinal properties of the genusAchillea.DARU Journal of Pharmaceutical Sciences, 19(3), 173–186.https://pmc.ncbi.nlm.nih.gov/articles/PMC3232110/
- **DOI Status**: `MISSING`
- **DOI Issues**: No DOI present in reference

#### Reference 14.html.9
- **Reference Text**: Yaeesh, S., Jamal, Q., Khan, A.-U., & Gilani, A. H. (2006). Studies on hepatoprotective, antispasmodic and calcium antagonist activities of the aqueous–methanol extract ofAchillea millefolium.Phytotherapy Research, 20(7), 546–551.https://doi.org/10.1002/ptr.1897
- **DOI Status**: `OK`
- **Existing DOI**: `10.1002/ptr.1897`

