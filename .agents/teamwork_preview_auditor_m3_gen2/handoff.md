# Milestone 3 Forensic Integrity Audit Report (Chapters 01–20)

## 🔒 Verdict: INTEGRITY VIOLATION

---

## 1. Observation

Direct empirical observations from `chapters/chapter_01.html` through `chapters/chapter_20.html`:

### A. Hallucinated DOI Mismatches (Fake / Mismatched References)
1. **`chapters/chapter_02.html` (Lines 1325–1335, Ref 9)**:
   - **Cited Text**: `Juríková, T., Mlcek, J., Skrovankova, S., Balla, S., & Sochor, J. (2018). Amelanchier alnifolia: A rich source of biologically active compounds with high antioxidant capacity. Nutrients, 10(11), 1753.`
   - **Embedded Link**: `<a href="https://doi.org/10.3390/nu10111753">https://doi.org/10.3390/nu10111753</a>`
   - **Actual DOI Target**: *"Comment on: The Vitamin D–Folate Hypothesis as an Evolutionary Model for Skin Pigmentation: An Update and Integration of Current Ideas, Nutrients 2018, 10, 554"* (Similarity score: **0.24**).
   - **Violation**: The inserted DOI points to an unrelated comment paper about skin pigmentation and vitamin D.

2. **`chapters/chapter_02.html` (Lines 1349–1358, Ref 11)**:
   - **Cited Text**: `Ozga, J. A., Saeed, A., Wismer, W. V., & Reinecke, D. M. (2018). Flavonoid profile and antioxidant activity of Saskatoon (Amelanchier alnifolia Nutt.) berries. Journal of Agricultural and Food Chemistry, 66(15), 3942–3951.`
   - **Embedded Link**: `<a href="https://doi.org/10.1021/acs.jafc.8b01183">https://doi.org/10.1021/acs.jafc.8b01183</a>`
   - **Actual DOI Target**: *"An Extensive Description of the Peptidomic Repertoire of the Hen Egg Yolk Plasma"* (Similarity score: **0.19**).
   - **Violation**: The inserted DOI points to a paper on hen egg yolk plasma.

3. **`chapters/chapter_02.html` (Lines 1420, Ref 17)**:
   - **Cited Text**: `Zatylny, A. M., Ziehl, W. D., & St-Pierre, R. G. (2018). Phytochemical composition and antioxidant activity of Saskatoon berry cultivars...`
   - **Embedded Link**: `<a href="https://doi.org/10.1016/j.foodchem.2017.05.041">https://doi.org/10.1016/j.foodchem.2017.05.041</a>`
   - **Actual DOI Target**: *"Polysaccharides from by-products of the Wonderful and Laffan pomegranate varieties: New insight into extraction and characterization"* (Similarity score: **0.15**).
   - **Violation**: The inserted DOI points to pomegranate extraction research.

4. **`chapters/chapter_03.html` (Lines 494–501, Ref 1)**:
   - **Cited Text**: `Böttger, S., & Melzig, M. F. (2013). The influence of saponins on cell membrane cholesterol. Bioorganic & Medicinal Chemistry, 21(22), 7118–7124.`
   - **Embedded Link**: `<a href="https://doi.org/10.1016/j.bmc.2013.09.011">https://doi.org/10.1016/j.bmc.2013.09.011</a>`
   - **Actual DOI Target**: *"In vitro structure–activity relationships of aplysinopsin analogs and their in vivo evaluation in the chick anxiety–depression model"* (Similarity score: **0.18**).
   - **Violation**: The inserted DOI points to aplysinopsin analogs in chick anxiety models.

5. **`chapters/chapter_03.html` (Lines 656, Ref 17)**:
   - **Cited Text**: `Upadhyay, A., & Singh, D. K. (2011). Pharmacological effects of Sapindus mukorossi...`
   - **Embedded Link**: `<a href="https://doi.org/10.1590/S0036-46652011000500004">https://doi.org/10.1590/S0036-46652011000500004</a>`
   - **Actual DOI Target**: *"Effect of bioactive compounds extracted from euphorbious plants on hematological and biochemical parameters of Channa punctatus"* (Similarity score: **0.21**).
   - **Violation**: The inserted DOI points to Channa punctatus fish research.

6. **`chapters/chapter_05.html` (Lines 402, Ref 4)**:
   - **Cited Text**: `Ganzera, M., Egger, C., Zidorn, C., & Stuppner, H. (2008). Quantitative analysis of flavonoids and saponins...`
   - **Embedded Link**: `<a href="https://doi.org/10.1016/j.aca.2008.03.009">https://doi.org/10.1016/j.aca.2008.03.009</a>`
   - **Actual DOI Target**: *"Studies on the mechanism of the peroxyoxalate chemiluminescence reaction"* (Similarity score: **0.19**).
   - **Violation**: The inserted DOI points to peroxyoxalate chemiluminescence reactions.

7. **`chapters/chapter_05.html` (Lines 439, Ref 7)**:
   - **Cited Text**: `Klaas, C. A., Wagner, G., Laufer, S., Sosa, S., Della Loggia, R., Bomme, U., & Merfort, I. (2002)...`
   - **Embedded Link**: `<a href="https://doi.org/10.1055/s-2002-26747">https://doi.org/10.1055/s-2002-26747</a>`
   - **Actual DOI Target**: *"Diphyllin Acetylapioside, A 5-Lipoxygenase Inhibitor from Haplophyllum hispanicum"* (Similarity score: **0.16**).

8. **`chapters/chapter_05.html` (Lines 454, Ref 8)**:
   - **Cited Text**: `Kriplani, P., Guarve, K., & Baghael, U. S. (2017). Arnica montana L.—A plant of healing...`
   - **Embedded Link**: `<a href="https://doi.org/10.1111/jphp.12735">https://doi.org/10.1111/jphp.12735</a>`
   - **Actual DOI Target**: *"Phytochemical and biological studies of Atriplex inflata f. Muell.: isolation of secondary bioactive metabolites"* (Similarity score: **0.16**).

---

### B. Broken DOIs (Resolution Failures / 404 Not Found)
1. **`chapters/chapter_01.html` (Line 114, Ref 4)**:
   - **DOI**: `10.1890/1051-0761(2000)010` (Truncated / malformed string). Resolution returns **HTTP 404 Not Found**.
2. **`chapters/chapter_03.html` (Line 508, Ref 2)**:
   - **DOI**: `10.1155/2020/8817078`. Resolution returns **HTTP 404 Not Found**.

---

### C. HTML Cleanliness & Structure Violations
1. **`chapters/chapter_01.html` (Line 114)**:
   - **Verbatim Code**:
     ```html
     (5), 1275–1287. <a href="https://doi.org/">https://doi.org/</a><a href="https://doi.org/10.1890/1051-0761(2000)010[1275:tekawo]2.0.co;2">https://doi.org/10.1890/1051-0761(2000)010[1275:tekawo]2.0.co;2</a>
     ```
   - **Violation**: Contains a stray empty prefix tag `<a href="https://doi.org/">https://doi.org/</a>` prepended to the link.

2. **`chapters/chapter_03.html` (Line 508)**:
   - **Verbatim Code**:
     ```html
     <li>
        Elbandy, M. (2020). Saponins and their potential role in diabetes mellitus. <em>Advances in Pharmacological and Pharmaceutical Sciences, 2020</em>, Article 8817078. https://doi.org/10.1155/2020/8817078
     </li>
     ```
   - **Violation**: Unhyperlinked plain text DOI string (`https://doi.org/10.1155/2020/8817078`) missing an `<a href="...">` anchor wrapper.

---

## 2. Logic Chain

1. **Premise 1**: A valid reference link must point authentically to the paper cited in the text and return a 200 OK HTTP status from DOI resolution services (CrossRef / doi.org).
2. **Observation 1**: Across Chapters 02, 03, and 05, multiple DOI links map to entirely unrelated research articles (e.g. Hen Egg Yolk Plasma, Pomegranate extraction, Vitamin D comments, Aplysinopsin analogs in chick anxiety, Atriplex inflata). The title similarity between the cited paper and the target DOI paper is below 0.25 (15% - 24%).
3. **Conclusion 1**: These DOIs were hallucinated or randomly assigned without verifying the true target paper, constituting a **hallucinated implementation / fake reference integrity violation**.
4. **Premise 2**: HTML markup in reference sections must be clean, valid, properly hyperlinked, and free of empty anchor tags or unhyperlinked URLs.
5. **Observation 2**: Chapter 01 line 114 contains a duplicate broken anchor tag `<a href="https://doi.org/">https://doi.org/</a>`, and Chapter 03 line 508 contains plain unhyperlinked text `https://doi.org/10.1155/2020/8817078` that resolves to HTTP 404.
6. **Conclusion 2**: The HTML structure fails cleanliness and formatting standards.
7. **Final Logical Deduction**: Because both behavioral resolution (hallucinated DOIs and 404 errors) and structural cleanliness checks failed, the overall work product fails the Forensic Integrity Audit.

---

## 3. Caveats

- **Network Limits**: Live HTTP resolution to CrossRef/doi.org was checked against pre-cached CrossRef response logs from audit runs, supplemented by static regex and string similarity analysis.
- **Scope**: Audit was focused on reference sections in `chapter_01.html` through `chapter_20.html`. Remaining chapters (21-50+) were outside Milestone 3 scope.

---

## 4. Conclusion & Explicit Verdict

### **VERDICT: INTEGRITY VIOLATION**

The reference additions in Milestone 3 (Chapters 01–20) contain multiple critical integrity violations:
1. **8+ Hallucinated DOI Mismatches** where inserted links lead to unrelated academic papers.
2. **2 Broken DOIs** returning 404 Not Found.
3. **2 HTML Structure Defect Instances** (stray empty DOI anchor tags and unhyperlinked DOI URLs).

The implementation is **REJECTED** and must be remediated before Milestone 3 can be certified.

---

## 5. Verification Method

To independently verify these findings, perform the following steps:

1. **Inspect Chapter 01 (Line 114)**:
   - File: `chapters/chapter_01.html`
   - Observe stray `<a href="https://doi.org/">` tag.

2. **Inspect Chapter 02 (Line 1334 & Line 1358)**:
   - File: `chapters/chapter_02.html`
   - Test DOI resolution for `10.3390/nu10111753` (resolves to Vitamin D Comment paper instead of *Amelanchier alnifolia*).
   - Test DOI resolution for `10.1021/acs.jafc.8b01183` (resolves to Hen Egg Yolk Plasma instead of Saskatoon berries).

3. **Inspect Chapter 03 (Lines 494–508)**:
   - File: `chapters/chapter_03.html`
   - Test DOI resolution for `10.1016/j.bmc.2013.09.011` (resolves to aplysinopsin analogs instead of saponins/cholesterol).
   - Check line 508 for raw text `https://doi.org/10.1155/2020/8817078` without an `<a>` tag and note HTTP 404.

4. **Invalidation Condition**:
   - The verdict changes to CLEAN if and only if all hallucinated DOIs are replaced with genuine matching DOIs, broken links are fixed to return HTTP 200 OK with matching metadata, and HTML tags are sanitized across Chapters 01–20.
