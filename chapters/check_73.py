import urllib.request, json, urllib.parse
title = 'A systematic review on the chemical constituents of the genus Delphinium and their biological activities'
url = f'https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(title)}&select=DOI,title&rows=5'
req_headers = {'User-Agent': 'mailto:test@example.com'}
req = urllib.request.Request(url, headers=req_headers)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    items = data.get('message', {}).get('items', [])
    for i, item in enumerate(items):
        print(f'{i}: {item.get("DOI")} - {item.get("title", [""])[0]}')
