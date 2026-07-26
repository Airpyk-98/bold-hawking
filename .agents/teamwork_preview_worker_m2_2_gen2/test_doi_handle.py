import urllib.request, urllib.error, ssl

ssl._create_default_https_context = ssl._create_unverified_context

class NoRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirection)
headers = {'User-Agent': 'Mozilla/5.0'}

test_dois = [
    "10.1002/ptr.1110",            # Filipowicz 2003 (valid)
    "10.1093/ecam/neh072",          # Adams 2005 (valid)
    "10.1007/s40268-016-0157-5",    # Lopresti 2017 (valid)
    "10.1021/jf100082p",            # Ramos 2010 (valid)
    "10.1055/s-2000-11117",         # Konrad 2000 (valid)
    "10.1007/BF02860489",           # Timbrook 1990 (valid)
    "10.1007/s40268-016-0157-8",    # Broken DOI (404)
    "10.1021/jf100871b",            # Broken DOI (404)
    "10.1055/s-2000-11120",         # Wrong/hallucinated (resolved to Harrisonia abyssinica)
]

for d in test_dois:
    url = f"https://doi.org/{d}"
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = opener.open(req, timeout=5)
        print(f"DOI {d:30s} -> HTTP {resp.getcode()}")
    except urllib.error.HTTPError as e:
        print(f"DOI {d:30s} -> HTTP {e.code}")
    except Exception as e:
        print(f"DOI {d:30s} -> ERROR {e}")
