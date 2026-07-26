# Project Plan: Reference Verification and Correction (Chapters 1-20)

## Architecture & Workflows
- **Scope**: `chapters/chapter_01.html` through `chapters/chapter_20.html` in `C:\Users\DELL\Documents\antigravity\bold-hawking`.
- **Target**: Extract references, query CrossRef API / search for real DOIs & URLs, verify title matching to prevent hallucinated DOIs, rewrite HTML reference tags with clean anchor tags (`<a href="https://doi.org/...">...</a>`), remove hallucinated DOIs where no true DOI exists, verify HTTP 200 status for all DOI links, conduct forensic audit, commit and push to `main` branch.

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Exploration & Reference Extraction | Chapters 1-20 reference parsing & inventory | None | DONE |
| 2 | Reference CrossRef Verification & HTML Correction | Query CrossRef API, check title match, correct HTML | M1 | DONE |
| 3 | Validation & Forensic Audit | Verify 200 OK for all DOIs, title alignment, clean HTML, no hallucinated DOIs | M2 | IN_PROGRESS |
| 4 | Git Commit & Push to Main | Commit all chapter changes & push to main branch on GitHub | M3 | PLANNED |

## Code Layout
- HTML files: `chapters/chapter_01.html` .. `chapters/chapter_20.html`
- Scripts & Utilities: Created by workers in workspace root or sub-directories as appropriate.
- State Files: `.agents/orchestrator/`
