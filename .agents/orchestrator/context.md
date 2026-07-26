# Context Documentation

## Project Overview
The `bold-hawking` project consists of HTML chapter files (`chapters/chapter_01.html` through `chapters/chapter_20.html` and beyond).
The goal is to inspect Chapters 1-20, extract all citations/references, query CrossRef API or web sources to verify paper titles, find genuine DOIs/URLs, update HTML files with proper anchor tags, strip hallucinated DOIs, verify 200 OK HTTP statuses, run forensic integrity checks, and push changes to GitHub.

## Key Files & Requirements
- Target Files: `chapters/chapter_01.html` to `chapters/chapter_20.html`
- CrossRef API: Query by title and authors.
- Strict Title Matching: Check fuzzy or normalized title match between CrossRef result and cited reference to avoid linking hallucinated DOIs.
- Clean Anchor Tags: Format as `<a href="https://doi.org/...">https://doi.org/...</a>` or appropriate clean text.
- Removal of Hallucinated DOIs: Remove DOI link/text if paper has no true DOI.
- Validation: 200 OK HTTP verification for all DOIs in Chapters 1-20.
- Report Generation: Document replaced/removed hallucinated DOIs.
- Git: Commit & Push to `main`.
