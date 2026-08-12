from pathlib import Path
import html, re, markdown
MAIN = 'Before_the_Name_1880-1969.md'
ADDENDA = ['Before_the_Name_image_links_appendix.md', 'audiovisual-reference-addendum-1880-1969.md', 'Before_the_Name_combined_addendum.md']
def chapter_slice(text):
    start = text.index('## Chapter 3 — 1890–1899: The Trial That Named a World')
    end = text.index('## Chapter 4 — 1900–1909:', start)
    return text[start:end].strip()
def relevant(text):
    match = re.search(r'(?im)^#{1,6} .*?(?:chapter\s*3|1890[–-]1899|trial)\b.*$', text)
    if not match:
        return ''
    following = re.search(r'(?m)^#{1,6} ', text[match.end():])
    return text[match.start():match.end()+following.start()] if following else text[match.start():]
def cards(texts):
    seen, output = set(), []
    for text in texts:
        for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', text):
            if url in seen:
                continue
            seen.add(url)
            low = url.lower().split('?')[0]
            title, href = html.escape(label), html.escape(url, quote=True)
            if low.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                media = f'<img src="{href}" alt="{title}" loading="lazy">'
            elif low.endswith(('.mp4', '.webm')):
                media = f'<video controls preload="metadata"><source src="{href}"></video>'
            elif low.endswith(('.mp3', '.ogg', '.wav')):
                media = f'<audio controls preload="metadata"><source src="{href}"></audio>'
            else:
                media = ''
            output.append(f'<article class="media-reference">{media}<h3>{title}</h3><p><a href="{href}">Source, media reference, and rights note</a></p></article>')
    return ''.join(output)
chapter = chapter_slice(Path(MAIN).read_text(encoding='utf-8'))
content = markdown.markdown(chapter, extensions=['extra', 'sane_lists'])
media = cards([chapter, *[relevant(Path(path).read_text(encoding='utf-8')) for path in ADDENDA]])
out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 — 1890–1899: The Trial That Named a World | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page chapter">{content}<section><h2>Media references</h2><p>Direct media files are embedded when available; archive and discovery sources remain linked with item-level rights notes.</p><div class="media-grid">{media}</div></section><nav class="chapter-nav"><a href="chapter-02-1880s.html">← Previous chapter</a><a href="chapter-04-1900s.html">Next chapter →</a></nav></main><footer class="site-footer">Early Queer History · Chapter 3</footer></body></html>'''
Path('chapter-03-1890s.preview.html').write_text(out, encoding='utf-8')