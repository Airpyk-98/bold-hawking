import os
import re
from html.parser import HTMLParser

CHAPTERS_DIR = r"C:\Users\DELL\Documents\antigravity\bold-hawking\chapters"
TARGET_CHAPTERS = [f"chapter_{i:02d}.html" for i in range(1, 21)]

class SyntaxChecker(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tag_stack = []
        self.nested_anchors = []
        self.syntax_errors = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if 'a' in self.tag_stack:
                self.nested_anchors.append({
                    'file': self.filename,
                    'line': self.getpos()[0],
                    'col': self.getpos()[1],
                    'tag': tag
                })
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.tag_stack:
            while self.tag_stack:
                popped = self.tag_stack.pop()
                if popped == tag:
                    break
        else:
            self.syntax_errors.append({
                'file': self.filename,
                'line': self.getpos()[0],
                'col': self.getpos()[1],
                'error': f"Unmatched closing tag </{tag}>"
            })

def main():
    print("=== FAST OFFLINE SYNTAX & DOI EXTRACTION ===")
    total_dois = 0
    all_dois = set()
    doi_by_chapter = {}
    nested_anchors_all = []
    syntax_errors_all = []

    for chapter_file in TARGET_CHAPTERS:
        file_path = os.path.join(CHAPTERS_DIR, chapter_file)
        if not os.path.exists(file_path):
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check nested anchor with regex
        # <a> tag containing another <a> before </a>
        nested_regex = r'<a\b[^>]*>(?:(?!</a>).)*?<a\b[^>]*>'
        regex_matches = re.findall(nested_regex, content, re.IGNORECASE | re.DOTALL)
        if regex_matches:
            nested_anchors_all.append((chapter_file, len(regex_matches), "Regex match"))

        # HTML parser
        parser = SyntaxChecker(chapter_file)
        try:
            parser.feed(content)
            if parser.nested_anchors:
                nested_anchors_all.append((chapter_file, len(parser.nested_anchors), parser.nested_anchors))
            if parser.syntax_errors:
                syntax_errors_all.append((chapter_file, parser.syntax_errors))
        except Exception as e:
            syntax_errors_all.append((chapter_file, str(e)))

        # Extract DOIs
        # href containing doi.org
        href_dois = re.findall(r'href=["\']([^"\']*doi\.org[^"\']*)["\']', content, re.IGNORECASE)
        # raw text doi links
        text_dois = re.findall(r'https?://(?:dx\.)?doi\.org/[^\s<>"\'\]]+', content, re.IGNORECASE)
        cleaned_text_dois = [u.rstrip('.,;)') for u in text_dois]
        
        combined_dois = sorted(list(set(href_dois + cleaned_text_dois)))
        doi_by_chapter[chapter_file] = combined_dois
        for d in combined_dois:
            all_dois.add(d)
        total_dois += len(combined_dois)

    print(f"Chapters Scanned: {len(TARGET_CHAPTERS)}")
    print(f"Total DOI link instances across chapters 1-20: {total_dois}")
    print(f"Total Unique DOI URLs: {len(all_dois)}")
    print(f"Nested Anchor Violations Found: {len(nested_anchors_all)}")
    if nested_anchors_all:
        for item in nested_anchors_all:
            print(f"  - {item}")
    print(f"HTML Syntax Errors Found: {len(syntax_errors_all)}")
    if syntax_errors_all:
        for item in syntax_errors_all:
            print(f"  - {item}")

    print("\nDOI Breakdown per Chapter:")
    for ch, dlist in doi_by_chapter.items():
        print(f"  {ch}: {len(dlist)} DOIs")

if __name__ == '__main__':
    main()
