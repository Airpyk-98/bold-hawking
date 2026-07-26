import os
import glob
import re

base_dir = r"C:\Users\DELL\.gemini\antigravity\brain\6a70ced1-308c-4b55-8f91-d40f1d746322"
scratch_dir = os.path.join(base_dir, "scratch")
output_file = os.path.join(base_dir, "caption_errors.md")

files = glob.glob(os.path.join(scratch_dir, "report_chunk*.md"))

# Sort files by chunk number
def extract_num(f):
    match = re.search(r'report_chunk(\d+)\.md', f)
    return int(match.group(1)) if match else 0

files.sort(key=extract_num)

with open(output_file, 'w', encoding='utf-8') as out:
    out.write("# Visual Verification Image Errors\n\n")
    out.write("The following image caption mismatches were detected by the subagents:\n\n")
    for f in files:
        with open(f, 'r', encoding='utf-8') as infile:
            out.write(f"## Chunk {extract_num(f)}\n\n")
            out.write(infile.read())
            out.write("\n\n---\n\n")

print(f"Combined {len(files)} reports into {output_file}")
