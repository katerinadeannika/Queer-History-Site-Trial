from pathlib import Path
import re

FILES = [
    'Before_the_Name_image_links_appendix.md',
    'audiovisual-reference-addendum-1880-1969.md',
    'queer-history-daphne-du-maurier-and-screen-literary-figures-addendum.md',
    'queer-history-literary-and-hollywood-evidence-addendum-v2.md',
]
OUT = 'Before_the_Name_combined_addendum.md'

def norm(s):
    return re.sub(r'\s+', ' ', s).strip().casefold()

def chunks(text):
    return re.split(r'(?=^#{1,6} )', text, flags=re.M)

seen = set()
out = ['# Before the Name — Combined Addendum', '', 'Generated from the four editorial addendums. The main manuscript is not modified.', '']
for name in FILES:
    text = Path(name).read_text(encoding='utf-8')
    kept = []
    for chunk in chunks(text):
        key = norm(chunk)
        if key and key not in seen:
            seen.add(key)
            kept.append(chunk.strip())
    if kept:
        out += [f'<!-- Source: {name} -->', *kept, '']
Path(OUT).write_text('\n\n'.join(out).strip() + '\n', encoding='utf-8')
