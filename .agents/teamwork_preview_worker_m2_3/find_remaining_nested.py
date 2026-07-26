import json

with open(r"C:\Users\DELL\Documents\antigravity\bold-hawking\.agents\teamwork_preview_worker_m2_3\refs_dump_15_20.json", "r", encoding="utf-8") as f:
    refs = json.load(f)

print("Remaining nested anchor tags:")
for r in refs:
    if r["nested"]:
        print(f"Ch {r['chapter']} Ref {r['ref_num']:02d}: HREFs={r['hrefs']}")
        print(f"   RAW: {r['raw_html']}")
        print("-" * 60)
