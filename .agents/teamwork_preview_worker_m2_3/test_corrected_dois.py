import requests

dois_to_check = [
    ("Ch 15 Ref 03", "10.1080/13693780400004810"),
    ("Ch 15 Ref 05", "10.1007/bf00973103"),
    ("Ch 15 Ref 06", "10.5962/bhl.title.62043"),
    ("Ch 15 Ref 09", "10.1016/j.phymed.2009.10.002"),
    ("Ch 15 Ref 10", "10.1002/(SICI)1099-1573(199909)13:6<540::AID-PTR523>3.0.CO;2-J"),
    ("Ch 15 Ref 12", "10.1186/s12906-016-1128-7"),
    ("Ch 15 Ref 13", "10.1078/094471102321621322"),
    ("Ch 15 Ref 14", "10.1016/j.ejphar.2003.11.066"),
    ("Ch 17 Ref 05", "10.1128/am.15.4.819-821.1967"),
    ("Ch 17 Ref 06", "10.1007/s11101-020-09671-y"),
    ("Ch 17 Ref 07", "10.1074/jbc.M112.438515"),
    ("Ch 18 Ref 07", "10.1007/s11240-020-01971-7"),
    ("Ch 19 Ref 07", "10.1155/2020/1258707"),
    ("Ch 20 Ref 09", "10.1016/j.jfoodeng.2004.08.032"),
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("Testing resolution of corrected DOIs...")
for label, doi in dois_to_check:
    url = f"https://doi.org/{doi}"
    try:
        r = requests.get(url, headers=headers, allow_redirects=False, timeout=8)
        loc = r.headers.get("Location", "")
        print(f"{label} | DOI: {doi} -> Status: {r.status_code} | Redirect: {loc}")
    except Exception as e:
        print(f"{label} | DOI: {doi} -> Error: {e}")
