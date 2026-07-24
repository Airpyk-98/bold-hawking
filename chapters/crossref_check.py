import urllib.request
import json
import urllib.parse
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# List of broken DOIs from the output
broken_dois = [
    "10.1016/j.indcrop.2025.117425",
    "10.1016/S0731-7085(03)00213-0",
    "10.1073/pnas.91.6.2493",
    "10.1016/0031-9422(91)84277-R",
    "10.1080/14786419.2011.567434",
    "10.1007/s10354-004-0115-4",
    "10.3389/fphar.2022.9505094",
    "10.2174/1871520611313080008",
    "10.1124/pr.52.4.673",
    "10.1016/0031-9422(81)80031-U",
    "10.1007/s11101-023-09821-2",
    "10.1016/S0031-9422(00)82276-8"
]

print("Checking CrossRef for DOIs directly...")
for doi in broken_dois:
    try:
        url = f"https://api.crossref.org/works/{doi}"
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
        resp = urllib.request.urlopen(req, context=ctx)
        data = json.loads(resp.read().decode('utf-8'))
        print(f"DOI {doi} exists in CrossRef: {data['message']['title'][0]}")
    except Exception as e:
        print(f"DOI {doi} NOT FOUND in CrossRef: {e}")

