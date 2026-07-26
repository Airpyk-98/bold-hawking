import os
import re
import urllib.request
import json
from bs4 import BeautifulSoup
import difflib

CHAPTER_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"

def audit_chapters():
    total_refs = 0
    total_dois = 0
    total_nested_anchors = 0
    total_hardcoded_nums = 0
    chapter_reports = []
    all_doi_citations = []

    print("=== STARTING MILESTONE 3 AUDIT (CHAPTERS 1-20) ===")

    for ch in range(1, 21):
        filename = f"chapter_{ch:02d}.html"
        filepath = os.path.join(CHAPTER_DIR, filename)

        if not os.path.exists(filepath):
            print(f"ERROR: File missing {filename}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        # 1. Nested anchors check across entire HTML DOM
        nested_anchors = []
        for a in soup.find_all("a"):
            if a.find("a"):
                nested_anchors.append(str(a))
        
        # 2. Reference section check
        ref_heading = None
        for h in soup.find_all(["h1", "h2", "h3", "h4", "p", "strong"]):
            text = h.get_text(strip=True).lower()
            if "reference" in text:
                ref_heading = h.get_text(strip=True)
                break

        # Find reference list
        # Check for <ol> lists
        ol_lists = soup.find_all("ol")
        ref_lis = []
        if ol_lists:
            # Usually the last <ol> or <ol> under/after reference heading
            ref_ol = ol_lists[-1]
            ref_lis = ref_ol.find_all("li", recursive=False)
        elif "chapter_04" not in filename:
            print(f"WARNING: No <ol> found in {filename}!")

        # 3. Check hardcoded leading numbers in <li> text
        hardcoded_in_ch = 0
        for li in ref_lis:
            txt = li.get_text(strip=True)
            if re.match(r"^(\d+[\.\)]|\[\d+\])", txt):
                hardcoded_in_ch += 1

        # 4. Extract DOIs and clean anchor check
        dois_in_ch = []
        doi_pattern = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
        
        for li in ref_lis:
            li_text = li.get_text(strip=True)
            anchors = li.find_all("a")
            for a in anchors:
                href = a.get("href", "")
                a_text = a.get_text(strip=True)
                if "doi.org" in href or doi_pattern.search(href) or doi_pattern.search(a_text):
                    m = doi_pattern.search(href) or doi_pattern.search(a_text)
                    if m:
                        doi_str = m.group(0).rstrip(".,;")
                        dois_in_ch.append({
                            "doi": doi_str,
                            "href": href,
                            "a_text": a_text,
                            "li_text": li_text
                        })

        total_refs += len(ref_lis)
        total_dois += len(dois_in_ch)
        total_nested_anchors += len(nested_anchors)
        total_hardcoded_nums += hardcoded_in_ch

        ch_info = {
            "chapter": ch,
            "filename": filename,
            "ref_heading": ref_heading,
            "ref_count": len(ref_lis),
            "doi_count": len(dois_in_ch),
            "nested_anchors": len(nested_anchors),
            "hardcoded_nums": hardcoded_in_ch,
            "dois": dois_in_ch
        }
        chapter_reports.append(ch_info)
        all_doi_citations.extend(dois_in_ch)

        print(f"Ch {ch:02d}: Refs={len(ref_lis)}, DOIs={len(dois_in_ch)}, NestedAnchors={len(nested_anchors)}, HardcodedNums={hardcoded_in_ch}")

    print("\n--- SUMMARY METRICS ---")
    print(f"Total References: {total_refs}")
    print(f"Total DOIs Extracted: {total_dois}")
    print(f"Total Nested Anchors: {total_nested_anchors}")
    print(f"Total Hardcoded Line Nums: {total_hardcoded_nums}")

    with open("audit_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_refs": total_refs,
                "total_dois": total_dois,
                "total_nested_anchors": total_nested_anchors,
                "total_hardcoded_nums": total_hardcoded_nums
            },
            "chapters": chapter_reports
        }, f, indent=2)

if __name__ == "__main__":
    audit_chapters()
