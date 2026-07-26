# Comprehensive Reference Analysis: Chapters 15 through 20

**Explorer 3 (Milestone 1)**  
**Workspace**: `C:\Users\DELL\Documents\antigravity\bold-hawking`  
**Date**: July 25, 2026  

---

## 1. Executive Summary

An exhaustive forensic analysis of the reference sections in **Chapters 15 through 20** (`chapters/chapter_15.html` to `chapters/chapter_20.html`) was conducted. 

### Key Metrics
- **Total Chapters Examined**: 6 chapters (Ch 15–20)
- **Total References Extracted**: 65 reference entries
- **Journal Articles with DOIs**: 44 entries
- **Web Pages / Database URLs**: 7 entries
- **Books / Ethnographic Reports / Oral Teachings**: 14 entries
- **Nested Anchor Tag Errors**: **51 out of 51 linked references (100% of links)**
- **Explicit Numbering Prefixes in `<li>`**: 12 entries (100% of Chapter 20 references)
- **Missing DOIs/Links in Journal References**: 1 entry (Chapter 20, Ref 2: Dahmer & Scott 2010)
- **Truncated / Incomplete Reference Entries**: 1 entry (Chapter 20, Ref 4: Elders of Cayoose Creek)
- **UTF-8 Encoding Integrity**: All files are valid UTF-8; special characters (curly quotes, en-dashes, accented characters like *Özcan*, *Hacıseferoğulları*, *Svedström*, *D'Auria*, *Figueiró*, *Caramão*, *Böhm*, *Dröge*) are preserved in source files.

---

## 2. Inventory & Chapter-by-Chapter Reference Breakdown

### Chapter 15: Lavender Salve (*Lavandula angustifolia* / Desert Lavender)
**File**: `chapters/chapter_15.html`  
**Total References**: 17 entries  
**Preceding Element**: `<p>References</p>`  

| Ref # | Citation Summary | Link Status / DOI | Identified Issues |
|-------|------------------|-------------------|-------------------|
| 1 | Bean, L. J., & Saubel, K. S. (1972). *Temalpakh...* | None (Book) | Clean text; no link expected. |
| 2 | Cavanagh, H. M. A., & Wilkinson, J. M. (2002). *Phytother Res* | `10.1002/ptr.1103` | **Nested `<a>` tags** (`<a href=...><a href=...>...</a></a>`) |
| 3 | D'Auria, F. D., et al. (2005). *Med Mycol* | `10.1080/13693780400029112` | **Nested `<a>` tags** |
| 4 | Elders and Community members... (n.d.). *Oral teachings...* | None (Oral) | Clean text; space before period in title. |
| 5 | Elisabetsky, E., et al. (1995). *Neurochem Res* | `10.1007/BF00973171` | **Nested `<a>` tags** |
| 6 | Felter, H. W., & Lloyd, J. U. (1898). *King's American...* | `10.5962/bhl.title.62043` | **Nested `<a>` tags** (BHL title link) |
| 7 | Kane, C. W. (2011). *Medicinal plants of the American Southwest* | None (Book) | Clean text; no link expected. |
| 8 | Koulivand, P. H., et al. (2013). *Evid Based Complement...* | `10.1155/2013/681304` | **Nested `<a>` tags** |
| 9 | Linck, V. D. M., et al. (2010). *Phytomedicine* | `10.1016/j.phymed.2010.01.013` | **Nested `<a>` tags** |
| 10 | Lis-Balchin, M., & Hart, S. (1999). *Phytother Res* | `10.1002/(SICI)...3.0.CO;2-J` | **Nested `<a>` tags** + **Mismatched outer/inner href**: outer ends with `3.0.co;2-i` (incorrect character `i`), inner ends with `3.0.CO;2-J` (correct checksum `J`). |
| 11 | Moerman, D. E. (1998). *Native American ethnobotany* | None (Book) | Clean text; no link expected. |
| 12 | Mori, H. M., et al. (2016). *BMC Complement Altern Med* | `10.1186/s12906-016-1131-8` | **Nested `<a>` tags** |
| 13 | Peana, A. T., et al. (2002). *Phytomedicine* | `10.1078/0944-7113-00258` | **Nested `<a>` tags** |
| 14 | Peana, A. T., et al. (2003). *Eur J Pharmacol* | `10.1016/j.ejphar.2003.11.010` | **Nested `<a>` tags** |
| 15 | Prashar, A., et al. (2004). *Cell Prolif* | `10.1111/j.1365-2184.2004.00307.x` | **Nested `<a>` tags** |
| 16 | Silva Brum, L. F., et al. (2001). *Phytother Res* | `10.1023/a:1010904214482` | **Nested `<a>` tags** |
| 17 | Tisserand, R., & Young, R. (2014). *Essential oil safety* | None (Book) | Clean text; no link expected. |

---

### Chapter 16: Arrow-Leaved Balsamroot (*Balsamorhiza sagittata*)
**File**: `chapters/chapter_16.html`  
**Total References**: 9 entries  
**Preceding Element**: `<p>References</p>`  

| Ref # | Citation Summary | Link Status / DOI | Identified Issues |
|-------|------------------|-------------------|-------------------|
| 1 | Böhm, B. A., et al. (1989). *Phytochemistry* | `10.1016/0031-9422(89)80041-X` | **Nested `<a>` tags** |
| 2 | Burt, S. (2004). *Int J Food Microbiol* | `10.1016/j.ijfoodmicro.2004.03.022` | **Nested `<a>` tags** |
| 3 | Elders and Community members... (n.d.). | None (Oral) | Missing `Oral teachings and traditional knowledge.` title text compared to Ch 15. |
| 4 | Flora of North America (2020). *Balsamorhiza sagittata* | Web URL (`floranorthamerica.org`) | **Nested `<a>` tags** |
| 5 | Hehner, S. P., et al. (1998). *J Biol Chem* | `10.1074/jbc.273.3.1288` | **Nested `<a>` tags** |
| 6 | McWilliams, J. (2002). FEIS USDA | Web URL (`fs.usda.gov`) | **Nested `<a>` tags** |
| 7 | Mohamed, A. E.-H. H., et al. (2006). *Chem Pharm Bull* | `10.1248/cpb.54.152` | **Nested `<a>` tags** |
| 8 | Panche, A. N., et al. (2016). *J Nutr Sci* | `10.1017/jns.2016.41` | **Nested `<a>` tags** |
| 9 | Swor, K., et al. (2024). *Nat Prod Commun* | `10.1177/1934578X231225842` | **Nested `<a>` tags** |

---

### Chapter 17: Big Sagebrush (*Artemisia tridentata*)
**File**: `chapters/chapter_17.html`  
**Total References**: 10 entries  
**Preceding Element**: `<p>References</p>`  

| Ref # | Citation Summary | Link Status / DOI | Identified Issues |
|-------|------------------|-------------------|-------------------|
| 1 | Elders and Community members... (n.d.). | None (Oral) | Missing `Oral teachings and traditional knowledge.` title text. |
| 2 | Höld, K. M., et al. (2000). *Proc Natl Acad Sci USA* | `10.1073/pnas.070042397` | **Nested `<a>` tags** |
| 3 | Juergens, U. R. (2014). *Drug Res* | `10.1055/s-0034-1372609` | **Nested `<a>` tags** |
| 4 | Moerman, D. E. (n.d.). BRIT NAEB Database | Web URL (`naeb.brit.org`) | **Nested `<a>` tags** |
| 5 | Nagy, J. G., & Tengerdy, R. P. (1967). *Appl Microbiol* | `10.1128/am.15.4.819-821.1967` | **Nested `<a>` tags** |
| 6 | Patočka, J., & Navrátilová, Z. (2020). *Phytochem Rev* | `10.1007/s11101-020-09701-z` | **Nested `<a>` tags** |
| 7 | Selescu, T., et al. (2013). *J Biol Chem* | `10.1074/jbc.M112.438515` | **Nested `<a>` tags** |
| 8 | Shultz, L. M. (2006). Flora of North America | Web URL (`floranorthamerica.org`) | **Nested `<a>` tags** |
| 9 | Swor, K., et al. (2022). *Nat Prod Commun* | `10.1177/1934578X221117417` | **Nested `<a>` tags** |
| 10 | Zheljazkov, V. D., et al. (2022). *Plants* | `10.3390/plants11091228` | **Nested `<a>` tags** |

---

### Chapter 18: Birch Leaf Spirea (*Spiraea betulifolia*)
**File**: `chapters/chapter_18.html`  
**Total References**: 8 entries  
**Preceding Element**: `<p>References</p>`  

| Ref # | Citation Summary | Link Status / DOI | Identified Issues |
|-------|------------------|-------------------|-------------------|
| 1 | Elders and Community members... (n.d.). | None (Oral) | Missing `Oral teachings and traditional knowledge.` title text. |
| 2 | Kostikova, V. A., & Petrova, N. V. (2021). *Int J Mol Sci* | `10.3390/ijms222011163` | **Nested `<a>` tags** |
| 3 | Kostikova, V. A., & Shaldaeva, T. M. (2017). *Russ J Bioorg Chem* | `10.1134/S1068162017070081` | **Nested `<a>` tags** |
| 4 | Li, Y., et al. (2016). *Nutrients* | `10.3390/nu8030167` | **Nested `<a>` tags** |
| 5 | Lis, R. (2020). Flora of North America | Web URL (`floranorthamerica.org`) | **Nested `<a>` tags** |
| 6 | Moerman, D. E. (n.d.). NAEB BRIT | Web URL (`naeb.brit.org`) | **Nested `<a>` tags** |
| 7 | Muraseva, D. S., & Kostikova, V. A. (2021). *Plant Cell Tissue Organ Cult* | `10.1007/s11240-020-01971-7` | **Nested `<a>` tags** |
| 8 | Zheleznichenko, T. V., et al. (2023). *Int J Mol Sci* | `10.3390/ijms24032362` | **Nested `<a>` tags** |

---

### Chapter 19: Black Gooseberry (*Ribes lacustre*)
**File**: `chapters/chapter_19.html`  
**Total References**: 9 entries  
**Preceding Element**: `<p>References</p>`  

| Ref # | Citation Summary | Link Status / DOI | Identified Issues |
|-------|------------------|-------------------|-------------------|
| 1 | Elders and Community members... (n.d.). | None (Oral) | Missing `Oral teachings and traditional knowledge.` title text. |
| 2 | Kuhnlein, H. V. (1989). *J Food Compos Anal* | `10.1016/0889-1575(89)90059-8` | **Nested `<a>` tags** |
| 3 | Lhotská, I., et al. (2021). *Foods* | `10.3390/foods10081745` | **Nested `<a>` tags** |
| 4 | Li, S., et al. (2019). *Int J Mol Sci* | `10.3390/ijms20102588` | **Nested `<a>` tags** |
| 5 | Moyer, R. A., et al. (2002). *J Agric Food Chem* | `10.1021/jf011062r` | **Nested `<a>` tags** |
| 6 | Nohynek, L. J., et al. (2006). *Nutr Cancer* | `10.1207/s15327914nc5401_4` | **Nested `<a>` tags** |
| 7 | Santos, I. B. D. S., et al. (2020). *Adv Pharmacol Pharm Sci* | `10.1155/2020/1258707` | **Nested `<a>` tags** |
| 8 | Sun, Q., et al. (2021). *J Ethnopharmacol* | `10.1016/j.jep.2021.114166` | **Nested `<a>` tags** |
| 9 | Washington Native Plant Society (n.d.) | Web URL (`wnps.org`) | **Nested `<a>` tags** |

---

### Chapter 20: Black Hawthorn (*Crataegus douglasii*)
**File**: `chapters/chapter_20.html`  
**Total References**: 12 entries  
**Preceding Element**: `<p>References</p>`  

| Ref # | Citation Summary | Link Status / DOI | Identified Issues |
|-------|------------------|-------------------|-------------------|
| 1 | Alirezalu, A., et al. (2018). *Int J Food Prop* | `10.1080/10942912.2018.1446146` | **Nested `<a>` tags** + **Hardcoded `1. ` prefix in `<li>`** |
| 2 | Dahmer, S., & Scott, E. (2010). *Am Fam Physician* | None (Journal) | **Hardcoded `2. ` prefix** + **MISSING DOI/URL LINK** |
| 3 | Edwards, J. E., et al. (2012). *Phytochemistry* | `10.1016/j.phytochem.2012.04.006` | **Nested `<a>` tags** + **Hardcoded `3. ` prefix** |
| 4 | Elders and Community members... | None (Oral) | **Hardcoded `4. ` prefix** + **TRUNCATED ENTRY** (missing `(n.d.). Oral teachings...`) |
| 5 | Holubarsch, C. J. F., et al. (2008). *Eur J Heart Fail* | `10.1016/j.ejheart.2008.10.004` | **Nested `<a>` tags** + **Hardcoded `5. ` prefix** |
| 6 | Kuhnlein, H. V., & Turner, N. J. (1991). *Traditional plant foods...* | None (Book) | **Hardcoded `6. ` prefix** |
| 7 | Moerman, D. E. (2009). *Native American medicinal plants...* | None (Book) | **Hardcoded `7. ` prefix** |
| 8 | Nabavi, S. F., et al. (2015). *Nutrients* | `10.3390/nu7095361` | **Nested `<a>` tags** + **Hardcoded `8. ` prefix** |
| 9 | Özcan, M., et al. (2005). *J Food Eng* | `10.1016/j.jfoodeng.2004.08.024` | **Nested `<a>` tags** + **Hardcoded `9. ` prefix** |
| 10 | Svedström, U., et al. (2002). *Phytochemistry* | `10.1016/S0031-9422(02)00172-3` | **Nested `<a>` tags** + **Hardcoded `10. ` prefix** |
| 11 | Turner, N. J. (1995). *Food plants of coastal First Peoples* | None (Book) | **Hardcoded `11. ` prefix** |
| 12 | Yang, B., & Liu, P. (2012). *J Sci Food Agric* | `10.1002/jsfa.5671` | **Nested `<a>` tags** + **Hardcoded `12. ` prefix** |

---

## 3. Structural & Formatting Issues Analysis

### 1. Systemic Nested Anchor Tag Bug (`51/51` linked entries)
In every chapter, every reference containing a web link or DOI has been wrapped in a duplicate outer `<a>` tag:
```html
<!-- CURRENT MALFORMED STRUCTURE -->
<a href="https://doi.org/10.1002/ptr.1103">
<a href="https://doi.org/10.1002/ptr.1103">https://doi.org/10.1002/ptr.1103</a>
</a>
```
**Fix Strategy**: Clean all `<li>` nodes by unwrapping outer `<a>` tags and ensuring clean single anchor links:
```html
<!-- CORRECT STRUCTURE -->
<a href="https://doi.org/10.1002/ptr.1103" target="_blank" rel="noopener noreferrer">https://doi.org/10.1002/ptr.1103</a>
```

### 2. Hardcoded Number Prefixes in `<li>` (Chapter 20)
In `chapter_20.html`, every reference item inside `<ol>` contains a leading `N. ` string:
```html
<!-- CURRENT -->
<li>1. Alirezalu, A., ...</li>
<li>2. Dahmer, S., ...</li>
```
This causes double numbering in rendered HTML (`1. 1. Alirezalu...`).
**Fix Strategy**: Strip `^\d+\.\s*` from the beginning of each `<li>` item in Chapter 20.

### 3. Missing DOI/Link in Journal Article (Chapter 20, Ref 2)
Ref 2 in Chapter 20 (*Dahmer, S., & Scott, E. (2010). Health effects of hawthorn. American Family Physician, 81(4), 465–468.*) is missing a DOI link. 
*Note*: *American Family Physician* articles from 2010 do not have standard CrossRef DOIs. Recommended link: `<a href="https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html" target="_blank" rel="noopener noreferrer">https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html</a>` (or PMID: 20148500 permalink).

### 4. Truncated Indigenous Oral Teachings Entry (Chapter 20, Ref 4)
In Chapter 20, Ref 4 reads: `4. Elders and Community members of the Cayoose Creek Band of Sekw’el’was.`
It is missing `(n.d.). Oral teachings and traditional knowledge.`
**Fix Strategy**: Restore full standardized string: `Elders and Community members of the Cayoose Creek Band of Sekw’el’was. (n.d.). <em>Oral teachings and traditional knowledge</em>.`

### 5. Standardizing Reference Section Headings
Chapters 15–20 use `<p>References</p>` rather than standard HTML headings (`<h2 id="references">References</h2>`). Upgrading to standard `<h2 id="references">References</h2>` will ensure consistent DOM parsing and semantic HTML hierarchy across the monograph.

---

## 4. Verification & Recommendations for Milestone 2

1. **Automated Replacement Script**: Build an idempotent Python script (`apply_fixes_m1_3.py`) to process Chapters 15–20:
   - Fix nested `<a>` tags.
   - Remove hardcoded line number prefixes in `chapter_20.html`.
   - Update Chapter 20 Ref 2 with a valid link.
   - Restore truncated text in Chapter 20 Ref 4.
   - Standardize `<p>References</p>` to `<h2 id="references">References</h2>`.
2. **HTML Validation**: Run W3C HTML parser checks or Beautiful Soup validation to verify zero nested `<a>` tags remain.
3. **HTTP Status Check**: Ensure all 44 DOIs and 7 web URLs resolve with HTTP 200 status.
