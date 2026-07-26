import json

with open('full_doi_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items in audit: {len(data)}")

broken_or_search = []
valid_count = 0
no_doi_count = 0

for item in data:
    ch = item['chapter']
    rnum = item['ref_num']
    doi = item['existing_doi']
    status = item['status']
    cand = item['candidate']

    if status == 200:
        valid_count += 1
    elif doi:
        broken_or_search.append(item)
    else:
        no_doi_count += 1

print(f"Valid 200 DOIs: {valid_count}")
print(f"Items with broken/non-200 DOIs: {len(broken_or_search)}")
print(f"Items with no DOIs: {no_doi_count}")

print("\n--- Detailed Broken/Non-200 DOIs ---")
for item in broken_or_search:
    ch = item['chapter']
    rnum = item['ref_num']
    print(f"Ch {ch} Ref {rnum}: DOI='{item['existing_doi']}' Status={item['status']}")
    print(f"  Text: {item['text'][:100]}...")
    if item['candidate']:
        print(f"  Candidate: DOI='{item['candidate']['doi']}' Score={item['candidate']['score']:.2f} Title='{item['candidate']['title']}'")
    else:
        print("  Candidate: None")
