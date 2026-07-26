import os
import sys
import re
import json
import urllib.request
import urllib.parse
import urllib.error
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def string_similarity(a, b):
    a_clean = re.sub(r'[^\w\s]', '', a.lower()).strip()
    b_clean = re.sub(r'[^\w\s]', '', b.lower()).strip()
    return SequenceMatcher(None, a_clean, b_clean).ratio()

def check_doi_crossref_api(doi):
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
    doi_clean = doi_clean.rstrip('.\'")>]')
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                msg = data.get('message', {})
                titles = msg.get('title', [])
                title = titles[0] if titles else ""
                return 200, title, msg.get('DOI')
    except urllib.error.HTTPError as e:
        return e.code, None, None
    except Exception as e:
        return str(e), None, None
    return 404, None, None

def search_crossref_title(text):
    # Remove DOIs and URLs
    cleaned = re.sub(r'https?://\S+', '', text)
    cleaned = re.sub(r'10\.\d{4,9}/\S+', '', cleaned)
    cleaned = re.sub(r'^\d+[\.\)]\s*', '', cleaned).strip()
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(cleaned[:250])}&rows=3"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:verification@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            results = []
            for item in items:
                cand_doi = item.get('DOI')
                cand_titles = item.get('title', [])
                cand_title = cand_titles[0] if cand_titles else ""
                score = string_similarity(cleaned, cand_title)
                results.append({
                    'doi': cand_doi,
                    'title': cand_title,
                    'score': score
                })
            return results
    except Exception as e:
        print(f"CrossRef search error: {e}")
        return []

print("Helper functions defined.")
