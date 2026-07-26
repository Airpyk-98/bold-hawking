# Original User Request

## 2026-07-25T03:27:23Z

<USER_REQUEST>
You are the Project Orchestrator for the bold-hawking reference verification and correction project.

Working directory: C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\orchestrator
Project Root / Workspace: C:\Users\DELL\Documents\antigravity\bold-hawking
Original Request File: C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\ORIGINAL_REQUEST.md

Your task is to orchestrate and execute the requirements detailed in ORIGINAL_REQUEST.md:
1. Extract all references in Chapters 1-20 (chapters/chapter_01.html to chapters/chapter_20.html).
2. For each reference, query CrossRef API or web searches using title and authors to find true DOIs and URLs.
3. Perform strict integrity checks: title matching to prevent hallucinated DOIs from being linked.
4. Update HTML files with correct DOIs wrapped in proper `<a href="...">` anchor tags, clean up formatting, and remove hallucinated DOIs if no true DOI exists.
5. Verify that all doi.org links return 200 OK and sample check that DOIs match cited papers.
6. Commit changes and push to main branch on GitHub.
7. Maintain your plan.md, progress.md, and context.md in C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\orchestrator.
8. When all milestones are complete, send a message claiming completion to Sentinel.
</USER_REQUEST>
