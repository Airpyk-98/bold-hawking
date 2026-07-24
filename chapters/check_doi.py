import urllib.request, json
req_headers = {'User-Agent': 'mailto:test@example.com'}
dois = [
    '10.1039/c9ra10595d',
    '10.7324/JAPS.2013.31103',
    '10.1007/s00253-006-0314-x'
]
for doi in dois:
    try:
        url = f'https://api.crossref.org/works/{doi}'
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f'{doi} is valid: {data["message"]["title"][0]}')
    except Exception as e:
        print(f'{doi} error: {e}')
