import urllib.request
import re
import concurrent.futures
import time

BASE_URL = 'https://indigenousmedicinescayoosecreek.pressbooks.tru.ca/'

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def main():
    print("Fetching main page...")
    main_html = fetch_html(BASE_URL)
    
    # Extract TOC links
    # <p class="toc__title"><a href="...">
    pattern = r'<p class="toc__title">\s*<a href="([^"]+)">'
    links = re.findall(pattern, main_html)
    
    # Deduplicate while preserving order
    unique_links = []
    seen = set()
    for link in links:
        if link not in seen:
            unique_links.append(link)
            seen.add(link)
            
    print(f"Found {len(unique_links)} unique links in TOC.")
    
    final_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }
  img { max-width: 100%; height: auto; display: block; margin: 20px auto; }
  .stitched-page { margin-bottom: 60px; padding-bottom: 40px; border-bottom: 2px solid #ccc; }
  h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 0.5em; }
  h1.chapter-title { border-bottom: 1px solid #eee; padding-bottom: 10px; }
  h2 { color: #34495e; }
  .wp-caption { background: #f9f9f9; padding: 10px; border: 1px solid #ddd; text-align: center; margin-bottom: 20px; max-width: 100%; }
  .wp-caption-text { font-style: italic; color: #666; margin: 5px 0 0 0; }
  .chapter-nav { display: none !important; }
</style>
</head>
<body>
<div style="text-align:center; padding: 40px 0; border-bottom: 4px solid #2c3e50; margin-bottom: 40px;">
  <h1>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</h1>
  <p><em>Complete word-for-word single page compilation</em></p>
</div>
"""

    results = {}
    
    # Use ThreadPoolExecutor to fetch pages concurrently
    # Max workers = 10 to avoid overwhelming the server
    print("Fetching pages concurrently...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_html, url): url for url in unique_links}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                html = future.result()
                # Extract main content
                match = re.search(r'<main id="main"[^>]*>(.*?)</main>', html, re.IGNORECASE | re.DOTALL)
                if match:
                    results[url] = match.group(1)
                else:
                    results[url] = ""
                    print(f"No main content found for {url}")
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
                results[url] = ""

    print("Stitching pages...")
    for link in unique_links:
        content = results.get(link, "")
        if content:
            final_html += f'\n<div class="stitched-page">\n{content}\n</div>\n'

    final_html += '\n</body>\n</html>'

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Done! File saved to index.html")

if __name__ == '__main__':
    main()
