import urllib.request, json
url = 'https://api.crossref.org/works/10.1039/d0ra06811j'
req_headers = {'User-Agent': 'mailto:test@example.com'}
req = urllib.request.Request(url, headers=req_headers)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    item = data.get('message', {})
    authors = [a.get('family') for a in item.get('author', [])]
    print(f'Authors: {authors}')
    print(f'Page: {item.get("page")}, Issue: {item.get("issue")}, Volume: {item.get("volume")}')
