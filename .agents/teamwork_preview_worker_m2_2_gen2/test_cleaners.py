import re

def unwrap_nested_a(html):
    # Regex to find nested <a> tags: <a href="X"><a href="X">Y</a></a> or <a href="X">\n<a href="X">Y</a>\n</a>
    pattern = r'<a\s+href=["\']([^"\']+)["\']\s*>\s*<a\s+href=["\']([^"\']+)["\']\s*>(.*?)</a>\s*</a>'
    def repl(m):
        href1, href2, text = m.group(1), m.group(2), m.group(3)
        return f'<a href="{href1}">{text}</a>'
    return re.sub(pattern, repl, html, flags=re.DOTALL | re.IGNORECASE)

def fix_splitrock_href(html):
    # Malformed Splitrock hrefs match: <a href="&lt;a href=" https:="" splitrockenvironmental.ca"="">...
    # Replace malformed Splitrock anchor tags with correct single anchor tag
    pattern = r'<a\s+href=["\']&lt;a\s+href=.*?>'
    # Also handle nested splitrock hrefs
    html = re.sub(r'<a href="&lt;a href=" https:="" splitrockenvironmental\.ca""=""><a href="(https://splitrockenvironmental\.ca[^"]*)">.*?</a></a>([^"<>]*)("&gt;|">)?',
                  r'<a href="\1">\1\2</a>', html)
    html = re.sub(r'<a href="&lt;a href=" https:="" splitrockenvironmental\.ca""="">(https://splitrockenvironmental\.ca[^"]*)("&gt;|">)?',
                  r'<a href="\1">\1</a>', html)
    return html

# Test samples
sample_nested = '<a href="https://doi.org/10.1007/BF02858839">\n<a href="https://doi.org/10.1007/BF02858839">https://doi.org/10.1007/BF02858839</a>\n</a>'
print("Unwrapped nested test:")
print(unwrap_nested_a(sample_nested))
