# Original User Request

## 2026-07-25T02:26:53Z

<USER_REQUEST>
# Teamwork Project Prompt — Draft

> Status: Launched

Verify and correct all references in Chapters 1 through 20 of the `bold-hawking` manuscript by programmatically cross-referencing their titles with the CrossRef API and web searches to find the true, accurate DOIs and URLs.

Working directory: C:/Users/DELL/Documents/antigravity/bold-hawking
Integrity mode: development

## Requirements

### R1. Deep Extraction & Verification
Extract every single reference from `chapters/chapter_01.html` through `chapters/chapter_20.html`. For each reference, ignore the currently listed DOI/URL and use the paper's title and authors to query CrossRef or Google Search to find the actual, correct DOI. 

### R2. Strict Integrity Checking
Do not blindly accept DOIs that return a 200 HTTP status. You must verify that the title of the paper returned by CrossRef perfectly matches the reference cited in the text, to prevent hallucinated DOIs from being linked.

### R3. Implementation & Formatting Fixes
Update the HTML files with the correct DOIs wrapped in proper `<a href="...">` anchor tags. Fix any disorganized or mangled HTML formatting in the references section. If a true DOI absolutely cannot be found, remove the hallucinated DOI to prevent misleading links.

### R4. Version Control
Once all 20 chapters are rigorously verified and corrected, commit the changes and push them to the GitHub repository.

## Acceptance Criteria

### Verification & Accuracy
- [ ] A validation script confirms that every single `doi.org` link in Chapters 1-20 returns a `200 OK` status.
- [ ] A sample check confirms the DOIs point to the actual paper cited, not an unrelated paper.
- [ ] No mangled HTML anchor tags remain in the references section of Chapters 1-20.
- [ ] A report is generated documenting all the hallucinated/incorrect DOIs that were replaced.
- [ ] Changes are successfully pushed to `main`.
</USER_REQUEST>

## 2026-07-25T02:33:47Z


## 2026-07-25T02:46:45Z

Can you provide another status update? How is Milestone 2 (CrossRef verification and HTML anchor updates) progressing for Chapters 1-20? Are there any blockers?


