import json
import urllib.request
import urllib.error
import re
from difflib import SequenceMatcher

with open('audited_refs_ch1_7.json', 'r', encoding='utf-8') as f:
    audited = json.load(f)

print(f"Loaded {len(audited)} audited references.")

def check_doi_crossref_api(doi):
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
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

def check_doi_org_redirect(doi):
    doi_clean = re.sub(r'^https?://doi\.org/', '', doi).strip()
    url = f"https://doi.org/{doi_clean}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
    try:
        # Don't follow redirect, just see if doi.org redirects (301/302/303/307)
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def http_error_302(self, req, fp, code, msg, headers):
                return fp
            http_error_301 = http_error_302
            http_error_303 = http_error_302
            http_error_307 = http_error_302
            
        opener = urllib.request.build_opener(NoRedirectHandler)
        resp = opener.open(req, timeout=10)
        return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return str(e)

# Test existing DOIs
for ref in audited:
    ch = ref['chapter']
    rnum = ref['ref_num']
    text = ref['text']
    dois = ref['existing_dois']
    
    if dois:
        for doi in dois:
            cr_status, cr_title, cr_doi = check_doi_crossref_api(doi)
            red_status = check_doi_org_redirect(doi)
            print(f"Ch {ch} Ref {rnum}: DOI '{doi}' -> doi.org HEAD: {red_status}, CrossRef API: {cr_status}")
            if cr_title:
                print(f"   CrossRef Title: {cr_title[:80]}")
