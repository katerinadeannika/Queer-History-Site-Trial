from pathlib import Path
import html, re, markdown
MAIN = Path('Before_the_Name_1880-1969.md')
ADDENDA = ['Before_the_Name_image_links_appendix.md', 'audiovisual-reference-addendum-1880-1969.md', 'Before_the_Name_combined_addendum.md']
PAGES = {4:'chapter-04-1900s',5:'chapter-05-1910s',6:'chapter-06-1920s',7:'chapter-07-1930s',8:'chapter-08-1940s',9:'chapter-09-1950s',10:'chapter-10-1960s',11:'chapter-11-threads'}
def sections(text):
    matches = list(re.finditer(r'(?m)^## Chapter (\d+) — .+$', text))
    result = {}
    for i, match in enumerate(matches):
        number = int(match.group(1))
        if number in PAGES:
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            result[number] = text[match.start():end].strip()
    return result
def relevant(text, number):
    match = re.search(rf'(?im)^#{{1,6}} .*?(?:chapter\s*{number}\b|{number}0s|threads)\b.*$', text)
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
            low, title, href = url.lower().split('?')[0], html.escape(label), html.escape(url, quote=True)
            if low.endswith(('.jpg','.jpeg','.png','.gif','.webp')):
                media = f'<img src="{href}" alt="{title}" loading="lazy">'
            elif low.endswith(('.mp4','.webm')):
                media = f'<video controls preload="metadata"><source src="{href}"></video>'
            elif low.endswith(('.mp3','.ogg','.wav')):
                media = f'<audio controls preload="metadata"><source src="{href}"></audio>'
            else:
                media = ''
            output.append(f'<article class="media-reference">{media}<h3>{title}</h3><p><a href="{href}">Source, media reference, and rights note</a></p></article>')
    return ''.join(output)
source = MAIN.read_text(encoding='utf-8')
chapters = sections(source)
addenda = [Path(path).read_text(encoding='utf-8') for path in ADDENDA]
for number, slug in PAGES.items():
    chapter = chapters[number]
    heading = chapter.splitlines()[0].removeprefix('## ')
    body = markdown.markdown(chapter, extensions=['extra','sane_lists'])
    media = cards([chapter, *[relevant(text, number) for text in addenda]])
    previous = PAGES[number-1] if number > 4 else 'chapter-03-1890s'
    next_page = PAGES.get(number+1)
    next_link = f'<a href="{next_page}.html">Next chapter →</a>' if next_page else ''
    out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(heading)} | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page chapter">{body}<section><h2>Media references</h2><p>Direct media files are embedded when available; archive and discovery sources remain linked with item-level rights notes.</p><div class="media-grid">{media}</div></section><nav class="chapter-nav"><a href="{previous}.html">← Previous chapter</a>{next_link}</nav></main><footer class="site-footer">Early Queer History · Chapter {number}</footer></body></html>'''
    Path(f'{slug}.preview.html').write_text(out, encoding='utf-8')