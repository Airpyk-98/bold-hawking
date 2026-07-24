import urllib.request, json, urllib.parse

queries = {
    70: 'Effect of alcohol and aldehyde dehydrogenase inhibitors on the toxicity of 3-nitropropanol in rats',
    73: 'A systematic review on the chemical constituents of the genus Delphinium and their biological activities',
    74: 'The activity of cedar leaf oil vapor against respiratory viruses: Practical applications',
    76: 'Antimicrobial activity of resin acid derivatives'
}

req_headers = {'User-Agent': 'mailto:test@example.com'}

for chap, title in queries.items():
    url = f'https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(title)}&select=DOI,title&rows=3'
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            items = data.get('message', {}).get('items', [])
            if items:
                print(f'Chap {chap}: found DOI {items[0].get("DOI")} for {items[0].get("title", [""])[0]}')
            else:
                print(f'Chap {chap}: no results found')
    except Exception as e:
        print(f'Chap {chap} error: {e}')
