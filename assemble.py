import os
import re

base_dir = r"C:\Users\DELL\Documents\antigravity\bold-hawking"
chapters_dir = os.path.join(base_dir, "chapters")
index_file = os.path.join(base_dir, "index.html")
output_file = os.path.join(base_dir, "index_corrected.html")

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all <div class="stitched-page"> chunks
# The front matters are chapters too conceptually, or rather they are stitched pages
# We only want to replace the actual chapters.
# Let's see how many stitched pages there are in total.
# Let's just find where chapter 1 starts.
# Chapter 1 starts with '<section class="standard post-108 chapter type-chapter status-publish hentry" data-type="chapter">'

# Let's find the start of chapter 1 by searching for data-type="chapter" or "1 The importance of Soapberry"
match = re.search(r'<div class="stitched-page">\s*<div id="content"[^>]*>\s*<section[^>]*data-type="chapter"', content)
if not match:
    print("Could not find the start of chapter 1")
    exit(1)

start_idx = match.start()

# Let's keep the front matter
front_matter = content[:start_idx]

# We need to find where the chapters end and back matter starts, if any.
# In pressbooks, chapters are data-type="chapter". What's after the last chapter?
# Let's just grab the end of the last stitched-page or body tag.
# Actually, the 81 chapters are all the remaining stitched-pages until the back matter.
# Is there back matter? We can find the end of the last chapter.
# For safety, let's just assemble the front matter, then all 81 chapters, then any trailing HTML like </body></html>.
# Let's just extract the footer. The footer is just `</body>\n</html>`?
end_match = re.search(r'</body>\s*</html>', content)
if end_match:
    footer = content[end_match.start():]
else:
    footer = "</body>\n</html>"

# Are there any back-matter sections?
back_matter_match = re.search(r'<div class="stitched-page">\s*<div id="content"[^>]*>\s*<section[^>]*data-type="(back-matter|appendix|glossary)"', content[start_idx:])
if back_matter_match:
    # There is back matter, we should preserve it.
    back_matter_start = start_idx + back_matter_match.start()
    back_matter = content[back_matter_start:end_match.start() if end_match else len(content)]
else:
    # No back matter found
    back_matter = ""

# Now read all 81 chapters
chapters_content = ""
for i in range(1, 82):
    filename = os.path.join(chapters_dir, f"chapter_{i:02d}.html")
    with open(filename, 'r', encoding='utf-8') as f:
        chap_html = f.read()
        # Each chapter file only contains the <section>...</section>
        # We need to wrap it back in <div class="stitched-page"><div id="content" ...> 
        # Wait, does the chapter file contain the <div class="stitched-page">? 
        # Let's check chapter 1. It starts with <section class="standard post-108...
        
        # We need to wrap it just like the original file did:
        # <div class="stitched-page">
        #   <div id="content" class="site-content" tabindex="-1">
        #       <section ...> ... </section>
        #   </div>
        # </div>
        wrapped = f'<div class="stitched-page">\n\t<div id="content" class="site-content" tabindex="-1">\n\t\t\t{chap_html}\n\t</div><!-- #content -->\n</div>\n\n'
        chapters_content += wrapped

# Assemble everything
final_html = front_matter + chapters_content + back_matter + footer

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Successfully assembled index_corrected.html")
