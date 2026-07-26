# Reference Analysis Report: Chapters 1 through 7

**Author**: Explorer 1 (`teamwork_preview_explorer_m1_1`)  
**Scope**: `chapters/chapter_01.html` to `chapters/chapter_07.html`  
**Date**: 2026-07-25  

---

## Executive Summary

A comprehensive, automated, and manual audit of the reference sections across Chapters 1 through 7 of the *Bold Hawking* manuscript was conducted. A total of **84 references** were extracted and analyzed across these 7 chapters. 

Key Findings:
1. **Malformed Nested Anchor Tags**: **52 out of 84 references (61.9%)** contain severely corrupted nested `<a>` HTML tags of the form `<a href="..."><a href="...">URL</a></a>`. This HTML corruption breaks proper browser rendering and DOM traversal.
2. **Broken / Hallucinated DOIs**: **5 DOIs** returned HTTP 404 errors or contained hallucinated volume/ISBN/suffix parameters (e.g., Chapter 3 Ref #8, #12, #16, Chapter 1 Ref #4, Chapter 7 Ref #1).
3. **Missing / Unlinked DOIs**: **32 references (38.1%)** do not possess DOI links. While some are legitimate book publications, government reports, or Indigenous oral history communications, several journal articles lack DOIs or rely on plain-text URLs.
4. **Structural HTML Failures**:
   - **Chapter 5 (`chapter_05.html`)** references are completely missing an `<ol>` tag container; instead, 20 numbered paragraph (`<p>`) tags with inline line breaks (`<br>`) are used. Traditional scraper scripts looking for `<ol>` elements completely failed to extract Chapter 5.
   - **Chapter 4 (`chapter_04.html`)** contains 0 references (an introductory subsection without a reference list).

---

## High-Level Metrics Table

| Chapter File | H1 / Section Title | Total Refs | Nested `<a>` Tags | Missing / Unlinked DOIs | Broken (404) DOIs | HTML Structure Type |
|---|---|---|---|---|---|---|
| `chapter_01.html` | 1 Soapberry & Saskatoon (Cayoose Creek) | 4 | 2 | 3 | 1 | `<h2>References</h2>` + `<ol>` |
| `chapter_02.html` | 2 Saskatoon Berry | 18 | 17 | 7 | 0 | `<p><strong>References</strong></p>` + `<ol>` (#7) |
| `chapter_03.html` | 3 Soapberry | 19 | 14 | 5 | 4 | `<ol>` at end (No Heading) |
| `chapter_04.html` | 4 Introduction | 0 | 0 | 0 | 0 | No references present |
| `chapter_05.html` | 5 Arnica Salve/Rub | 20 | 0 | 10 | 0 | **Malformed Paragraph List** (`<p>` tags) |
| `chapter_06.html` | 6 Cottonwood Salve | 9 | 8 | 1 | 0 | `<p><strong>References</strong></p>` + `<ol>` (#7) |
| `chapter_07.html` | 7 Fir Tip Tea | 14 | 11 | 6 | 0 | `<p><strong>References</strong></p>` + `<ol>` (#4) |
| **TOTAL** | | **84** | **52** | **32** | **5** | |

---

## Detailed Audit by Chapter

### 1. Chapter 1: `chapters/chapter_01.html`
- **Title**: *1 The importance of Soapberry and Saskatoon berry to the Cayoose Creek Band*
- **Total References**: 4
- **Structural Findings**: Reference header is `<h2>References</h2>` followed by an `<ol>`.
- **Issues Identified**:
  - **Nested Anchor Tags**: Ref #2 and Ref #4 contain `<a href="..."><a href="...">...</a></a>`.
  - **Broken / Truncated DOI**:
    - **Ref #4**: `10.1890/1051-0761(2000)010` -> HTTP 404 (Truncated DOI). Real CrossRef DOI: `10.1890/1051-0761(2000)010[0539:TEKAWI]2.0.CO;2`.
  - **Missing DOIs**: Ref #1 (Book: *Traditional plant foods of Canadian indigenous peoples*), Ref #2 (Website: *Splitrock Environmental*), Ref #3 (Book: *Food plants of interior First Peoples*).

### 2. Chapter 2: `chapters/chapter_02.html`
- **Title**: *2 Saskatoon Berry*
- **Total References**: 18
- **Structural Findings**: Multiple `<ol>` elements in document (7 total). The main reference list is `<ol>` index 7 containing 18 `<li>` elements.
- **Issues Identified**:
  - **Nested Anchor Tags**: **17 out of 18 references** have double-wrapped anchor tags `<a href="https://doi.org/..."><a href="https://doi.org/...">...</a></a>`.
  - **Missing DOIs**: 7 items lack DOIs (Ref #1, #3, #4, #6, #12, #13, #15 - websites, extension guides, personal communications).

### 3. Chapter 3: `chapters/chapter_03.html`
- **Title**: *3 Soapberry*
- **Total References**: 19
- **Structural Findings**: `<ol>` element at the bottom of the section without an explicit `<h2>References</h2>` heading.
- **Issues Identified**:
  - **Nested Anchor Tags**: 14 references have nested `<a>` tags.
  - **Hallucinated / Broken (404) DOIs**:
    - **Ref #8**: `10.1021/jf0301506` -> HTTP 404. Real CrossRef DOI: `10.1021/jf0301910` (*Molluscicidal Saponins from Sapindus mukorossi*).
    - **Ref #12**: `10.1016/0308-8146(81)90068-5` -> HTTP 404. Real CrossRef DOI: `10.1016/0308-8146(81)90019-4` (*Saponins in food—A review*).
    - **Ref #16**: `10.1007/978-1-4899-1382-9_9` -> HTTP 404. Real CrossRef DOI: `10.1007/978-1-4613-0413-5_9` (*Saponins from Medicago*).
    - **Ref #14**: `10.3390/plants9020267` -> Points to wrong paper (*Carica papaya* review instead of *Sapindus mukorossi*).

### 4. Chapter 4: `chapters/chapter_04.html`
- **Title**: *4 Introduction*
- **Total References**: 0
- **Status**: Section introductory overview without a reference list.

### 5. Chapter 5: `chapters/chapter_05.html`
- **Title**: *5 Arnica Salve/Rub*
- **Total References**: 20
- **Structural Findings**: **CRITICAL FORMATTING DEFECT**. References are stored inside `<p>` blocks with line breaks `<br>` rather than a standard `<ol>` element.
- **Issues Identified**:
  - **Non-Standard HTML Structure**: Scrapers targeting `<ol>` miss all 20 references in Chapter 5. Needs conversion from raw paragraph list to `<ol><li>...</li></ol>`.
  - **Missing DOIs**: 10 out of 20 references (books, websites, traditional knowledge) lack DOIs.

### 6. Chapter 6: `chapters/chapter_06.html`
- **Title**: *6 Cottonwood Salve*
- **Total References**: 9
- **Structural Findings**: References header followed by `<ol>` (7th OL in doc).
- **Issues Identified**:
  - **Nested Anchor Tags**: **8 out of 9 references** have double `<a href="...">` tags.
  - **Missing DOIs**: Ref #3 (Indigenous traditional knowledge communication).

### 7. Chapter 7: `chapters/chapter_07.html`
- **Title**: *7 Fir Tip Tea*
- **Total References**: 14
- **Structural Findings**: Reference list inside `<ol>` index 4.
- **Issues Identified**:
  - **Nested Anchor Tags**: **11 out of 14 references** have nested `<a>` tags.
  - **Missing DOIs**: 6 references lack DOIs (Ref #2, #3, #4, #7, #10, #13).

---

## Workspace Scripts Audit

Existing workspace scripts were examined:
1. `extract_refs.py`: Targeted `index.html` or hardcoded chapter lists. Uses BeautifulSoup to search for `ol` after `References` text. Does not detect non-`<ol>` reference structures (like Chapter 5) and does not clean nested `<a>` tags.
2. `chapters/audit_refs.py`: Checks HTTP status of DOIs across `chapter_15.html` - `chapter_23.html`. Does not strip nested `<a>` tags before requesting URLs.
3. `chapters/check_crossref.py`: Demonstrates CrossRef API lookup for title verification.

---

## Actionable Recommendations for Implementers (Milestone 2)

1. **HTML Cleanup & Anchor Tag Normalization**:
   - Strip all outer duplicate `<a>` tags, standardizing on a single anchor tag:  
     `<a href="https://doi.org/<DOI>" target="_blank" rel="noopener noreferrer">https://doi.org/<DOI></a>`
2. **DOI Corrections**:
   - Chapter 1 Ref #4: Replace `10.1890/1051-0761(2000)010` with `https://doi.org/10.1890/1051-0761(2000)010[0539:TEKAWI]2.0.CO;2`.
   - Chapter 3 Ref #8: Replace `10.1021/jf0301506` with `https://doi.org/10.1021/jf0301910`.
   - Chapter 3 Ref #12: Replace `10.1016/0308-8146(81)90068-5` with `https://doi.org/10.1016/0308-8146(81)90019-4`.
   - Chapter 3 Ref #16: Replace `10.1007/978-1-4899-1382-9_9` with `https://doi.org/10.1007/978-1-4613-0413-5_9`.
3. **Restructure Chapter 5**:
   - Convert paragraph-based reference block into clean `<ol>` list structure under an `<h2>References</h2>` header.
