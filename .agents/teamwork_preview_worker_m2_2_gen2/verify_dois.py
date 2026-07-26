import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
import time
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

ssl._create_default_https_context = ssl._create_unverified_context
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
crossref_headers = {'User-Agent': 'mailto:worker_m2_2@example.com'}

def clean_str(s):
    if not s:
        return ""
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'[^\w\s]', '', s)
    return ' '.join(s.lower().split())

def title_similarity(t1, t2):
    c1 = clean_str(t1)
    c2 = clean_str(t2)
    if not c1 or not c2:
        return 0.0
    if c1 == c2:
        return 1.0
    w1 = set(c1.split())
    w2 = set(c2.split())
    if not w1 or not w2:
        return 0.0
    
    # Remove common citation stop words from comparison
    stopwords = {"journal", "study", "analysis", "review", "research", "effect", "effects", "human", "using", "between", "characterization", "the", "and", "of", "in", "for", "on", "a", "an"}
    w1_filt = w1 - stopwords
    w2_filt = w2 - stopwords
    
    if not w1_filt or not w2_filt:
        w1_filt, w2_filt = w1, w2
        
    intersection = w1_filt.intersection(w2_filt)
    smaller_len = min(len(w1_filt), len(w2_filt))
    overlap = len(intersection) / float(smaller_len)
    
    sm_ratio = SequenceMatcher(None, c1, c2).ratio()
    return max(overlap, sm_ratio)

def check_doi_http(doi):
    clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi).strip()
    url = f"https://doi.org/{clean_doi}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.getcode(), resp.geturl()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return str(e), None

def fetch_crossref_doi_metadata(doi):
    clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi).strip()
    url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi)}"
    req = urllib.request.Request(url, headers=crossref_headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            message = data.get('message', {})
            title = message.get('title', [''])[0]
            authors = []
            for a in message.get('author', []):
                authors.append(f"{a.get('given', '')} {a.get('family', '')}".strip())
            return {"valid": True, "title": title, "authors": authors, "doi": clean_doi}
    except urllib.error.HTTPError as e:
        return {"valid": False, "status": e.code, "doi": clean_doi}
    except Exception as e:
        return {"valid": False, "error": str(e), "doi": clean_doi}

def search_crossref_doi(citation_text):
    clean_text = re.sub(r'https?://[^\s]+', '', citation_text)
    clean_text = re.sub(r'10\.\d{4,9}/[^\s]+', '', clean_text).strip()
    
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(clean_text[:250])}&rows=5"
    req = urllib.request.Request(url, headers=crossref_headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            candidates = []
            for item in items:
                t = item.get('title', [''])[0]
                d = item.get('DOI', '')
                candidates.append({'title': t, 'doi': d})
            return candidates
    except Exception as e:
        return []

# Load chapter reference items
ch9_refs_docx = [
    "1. Akdemir, Z. S., Tatli, I. I., Saracoglu, I., & Ismailoglu, U. B. (2001). Polyphenolic compounds from Verbascum lasianthum and Verbascum urticaefolium . Turkish Journal of Chemistry, 25 (4), 415–420.",
    "2. Alipieva, K., Korkina, L., Orhan, I. E., & Georgiev, M. I. (2014). Verbascoside—A review of its occurrence, (bio)synthesis and pharmacological significance. Biotechnology Advances, 32 (6), 1065–1076. https://doi.org/10.1016/j.biotechadv.2014.07.001",
    "3. Dulger, B., & Gonuz, A. (2004). Antimicrobial activity of some Turkish medicinal plants. Pakistan Journal of Biological Sciences, 7 (9), 1559–1562. https://doi.org/10.3923/pjbs.2004.1559.1562",
    "4. Elders and Community Members of the Cayoose Creek Band of Sekw’el’was. (n.d.). Personal communication.",
    "5. Hamill, F. A., Apio, S., Mubiru, N. K., Mosango, M., Bukenya-Ziraba, R., Maganyi, O. W., & Soejarto, D. D. (2000). Traditional herbal drugs of southern Uganda, I. Journal of Ethnopharmacology, 70 (3), 281–300. https://doi.org/10.1016/S0378-8741(99)00230-7",
    "6. Jones, A. (2024). Medicinal herbs of western Canada (1st ed.). Nimbus Publishing.",
    "7. Kupeli, E., Kosar, M., Yesilada, E., Hüsnu Can Baser, K., & Başer, C. (2005). A comparative study on the anti-inflammatory, antinociceptive and antipyretic effects of isoquinoline alkaloids from the roots of Turkish Berberis species. Life Sciences, 72 (6), 645–657. https://doi.org/10.1016/j.lfs.2003.09.053",
    "8. McCutcheon, A. R., Roberts, T. E., Gibbons, E., Ellis, S. M., Babiuk, L. A., Hancock, R. E., & Towers, G. H. N. (1995). Antiviral screening of British Columbian medicinal plants. Journal of Ethnopharmacology, 49 (2), 101–110. https://doi.org/10.1016/0378-8741(95)01321-0",
    "9. Moerman, D. E. (1998). Native American ethnobotany . Timber Press.",
    "10. Riaz, M., Zia-Ul-Haq, M., & Jaafar, H. Z. E. (2013). Common mullein, pharmacological and chemical aspects. Revista Brasileira de Farmacognosia, 23 (6), 948–959. https://doi.org/10.1590/S0102-695X2013000600004",
    "11. Sarić-Kundalić, B., Dobeš, C., Klatte-Asselmeyer, V., & Saukel, J. (2010). Ethnobotanical study on medicinal use of wild and cultivated plants in middle, south and west Bosnia and Herzegovina. Journal of Ethnopharmacology, 131 (1), 33–55. https://doi.org/10.1016/j.jep.2010.05.061",
    "12. Sarrell, E. M., Mandelberg, A., & Cohen, H. A. (2001). Efficacy of naturopathic extracts in the management of ear pain associated with acute otitis media. Archives of Pediatrics & Adolescent Medicine, 155 (7), 796–799. https://doi.org/10.1001/archpedi.155.7.796",
    "13. Tatli, I. I., & Akdemir, Z. S. (2004). Traditional uses and biological activities of Verbascum species. FABAD Journal of Pharmaceutical Sciences, 29 , 85–96.",
    "14. Tatli, I. I., Akdemir, Z., Yesilada, E., & Küpeli, E. (2004). Anti-inflammatory and antinociceptive potential of major phenolics from Verbascum salviifolium . Zeitschrift für Naturforschung C, 59 (5–6), 609–613. https://doi.org/10.1515/znc-2004-5-622",
    "15. Turker, A. U., & Camper, N. D. (2002). Biological activity of common mullein, a medicinal plant. Journal of Ethnopharmacology, 82 (2–3), 117–125. https://doi.org/10.1016/S0378-8741(02)00159-3",
    "16. Zahradnik, H. P., & Goldmeier, S. (2020). Phytotherapy for dysmenorrhea, endometriosis, and premenstrual syndrome. In I. E. Orhan (Ed.), Herbal medicine (pp. 323–342). CRC Press. https://doi.org/10.1201/9780429243730-18",
    "17. Zgorniak-Nowosielska, I., Grzybek, J., Manolova, N., Serkedjieva, J., & Zawilinska, B. (1991). Antiviral activity of Flos Verbasci infusion against Influenza and Herpes simplex viruses. Archivum Immunologiae et Therapiae Experimentalis, 39 , 103–108.",
    "18. Zheleva-Dimitrova, D., Obreshkova, D., & Nedialkov, P. (2013). Antioxidant activity of iridoid glucosides from Veronica chamaedrys . Pharmacognosy Magazine, 9 (35), 268–273. https://doi.org/10.4103/0973-1296.113294"
]

all_results = {}

for ch in range(8, 15):
    filepath = f"chapters/chapter_{ch:02d}.html"
    print(f"\n========================================")
    print(f"Auditing DOIs for {filepath}...")
    
    items = []
    if ch == 9:
        for idx, text in enumerate(ch9_refs_docx):
            items.append({"num": idx+1, "text": text, "raw_html": f"<li>{text}</li>"})
    elif ch == 11:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        p_tags = soup.find_all('p')
        num_p = [p for p in p_tags if re.match(r'^\s*\d+\.\s+', p.get_text())]
        for idx, p in enumerate(num_p):
            items.append({"num": idx+1, "text": p.get_text().strip(), "raw_html": str(p)})
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        ol = soup.find_all('ol')[-1]
        lis = ol.find_all('li')
        for idx, li in enumerate(lis):
            items.append({"num": idx+1, "text": li.get_text().strip(), "raw_html": str(li)})
            
    ch_results = []
    for item in items:
        num = item["num"]
        text = item["text"]
        raw_html = item["raw_html"]
        
        # Extract existing DOI if present
        existing_doi = None
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', raw_html)
        if doi_match:
            existing_doi = doi_match.group(0).rstrip('.,;)"><')
        if not existing_doi:
            doi_match_text = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text)
            if doi_match_text:
                existing_doi = doi_match_text.group(0).rstrip('.,;)')
                
        final_doi = None
        status = "NO_DOI"
        notes = ""
        
        if existing_doi:
            # Check existing DOI
            code, _ = check_doi_http(existing_doi)
            meta = fetch_crossref_doi_metadata(existing_doi)
            if meta.get("valid"):
                sim = title_similarity(text, meta["title"])
                if code == 200 and sim >= 0.60:
                    status = "VALID_EXISTING"
                    final_doi = meta["doi"]
                    notes = f"DOI HTTP 200 OK, title match {sim:.2f}: '{meta['title']}'"
                elif code != 200:
                    status = "BROKEN_HTTP"
                    notes = f"Existing DOI HTTP {code}, metadata valid={meta.get('valid')}"
                else:
                    status = "HALLUCINATED"
                    notes = f"Existing DOI points to WRONG paper '{meta['title']}' (sim {sim:.2f})"
            else:
                status = "BROKEN_HTTP"
                notes = f"Existing DOI failed CrossRef metadata lookup"
                
        # If not VALID_EXISTING, search for candidate DOIs via CrossRef
        if status != "VALID_EXISTING":
            cands = search_crossref_doi(text)
            best_cand = None
            best_sim = 0.0
            for c in cands:
                sim = title_similarity(text, c["title"])
                if sim > best_sim:
                    best_sim = sim
                    best_cand = c
            
            if best_cand and best_sim >= 0.70:
                cand_doi = best_cand["doi"]
                code, _ = check_doi_http(cand_doi)
                if code == 200:
                    final_doi = cand_doi
                    if status == "HALLUCINATED":
                        status = "REPLACED_HALLUCINATED"
                    elif status == "BROKEN_HTTP":
                        status = "REPLACED_BROKEN"
                    else:
                        status = "ADDED_MISSING"
                    notes = f"Found true DOI via strict title match ({best_sim:.2f}): '{best_cand['title']}'"
                else:
                    notes += f" | Candidate DOI HTTP {code}"
            else:
                if status == "HALLUCINATED":
                    status = "REMOVED_HALLUCINATED"
                    notes += " | Removed hallucinated DOI (no true DOI found)"
                elif status == "BROKEN_HTTP":
                    status = "REMOVED_BROKEN"
                    notes += " | Removed broken DOI (no true DOI found)"
                else:
                    status = "NO_DOI"
                    notes = "No valid DOI found (likely book, website, or unindexed item)"
                    
        print(f"Ch{ch:02d} Ref #{num:02d}: Status={status:20s} | DOI={str(final_doi):35s} | Notes={notes[:80]}")
        ch_results.append({
            "num": num,
            "text": text,
            "existing_doi": existing_doi,
            "final_doi": final_doi,
            "status": status,
            "notes": notes
        })
        time.sleep(0.1)
        
    all_results[f"chapter_{ch:02d}"] = ch_results

with open(".agents/teamwork_preview_worker_m2_2_gen2/doi_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print("\nDOI Verification Complete! Saved to .agents/teamwork_preview_worker_m2_2_gen2/doi_audit_results.json")
