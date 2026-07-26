## 2026-07-25T02:42:29Z
You are Worker 1 (teamwork_preview_worker) assigned to Milestone 2: Reference Verification & HTML Correction for Chapters 1-7.

Working directory: C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_1
Explorer Handoff: C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_1\handoff.md
Analysis Report: C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_explorer_m1_1\analysis.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Task Instructions:
1. Read Explorer 1 handoff and analysis reports.
2. For chapters/chapter_01.html through chapters/chapter_07.html:
   - Format reference section into clean <ol><li> list items (convert raw <p> paragraphs in chapter_05.html).
   - Clean up nested duplicate <a> tags (<a href="..."><a href="...">...</a></a>) and mangled HTML formatting.
   - Cross-reference titles/authors against CrossRef API or search to find true DOIs.
   - Perform strict title matching (title similarity check) to verify candidate DOIs match cited paper.
   - Update HTML files with valid DOIs wrapped in proper <a href="https://doi.org/...">...</a> anchor tags.
   - Remove hallucinated/unverifiable DOIs where no true DOI exists.
3. Run build/test/verification scripts to verify all doi.org links in Chapters 1-7 return 200 OK status.
4. Record implementation details, replaced DOIs, and verification outputs in handoff.md in your working directory.
5. Update progress.md as you work.
6. Send completion message to parent (ID: a6f6f252-d601-4151-bc93-cb6f47865fe0).
