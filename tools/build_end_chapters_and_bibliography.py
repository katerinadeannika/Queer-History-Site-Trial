from pathlib import Path
import html, re, markdown
root = Path('.')
master = (root / 'Before_the_Name_complete_master.md').read_text(encoding='utf-8')
addenda = [p for p in root.glob('*.md') if 'addendum' in p.name.lower() or 'appendix' in p.name.lower()]
addendum_texts = [(p.name, p.read_text(encoding='utf-8')) for p in addenda]
chapter_matches = list(re.finditer(r'(?m)^## Chapter (\d+) — (.+)$', master))
def slug(number, title):
    decade = re.search(r'(\d{4})[–-](\d{4})', title)
    if decade:
        return f'chapter-{number:02d}-{decade.group(1)[:3]}0s'
    clean = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return f'chapter-{number:02d}-{clean[:48]}'
def media_cards(texts):
    seen, cards = set(), []
    for text in texts:
        for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', text):
            key = re.sub(r'[?#].*$', '', url.lower()).rstrip('/')
            if key in seen:
                continue
            seen.add(key)
            low, label, href = url.lower().split('?')[0], html.escape(label), html.escape(url, quote=True)
            if low.endswith(('.jpg','.jpeg','.png','.gif','.webp')):
                visual = f'<img src="{href}" alt="{label}" loading="lazy">'
            elif low.endswith(('.mp4','.webm')):
                visual = f'<video controls preload="metadata"><source src="{href}"></video>'
            elif low.endswith(('.mp3','.ogg','.wav')):
                visual = f'<audio controls preload="metadata"><source src="{href}"></audio>'
            else:
                visual = ''
            cards.append(f'<article class="media-reference">{visual}<h3>{label}</h3><p><a href="{href}">Source, media reference, and rights note</a></p></article>')
    return ''.join(cards)
for i, match in enumerate(chapter_matches):
    number, title = int(match.group(1)), match.group(2)
    if number < 12:
        continue
    end = chapter_matches[i+1].start() if i + 1 < len(chapter_matches) else len(master)
    text = master[match.start():end].strip()
    relevant = [text]
    for _, addendum in addendum_texts:
        if re.search(rf'(?im)^#{{1,6}} .*?(?:chapter\s*{number}\b|{number}0s|{re.escape(title.split(":")[0][:20])})', addendum):
            relevant.append(addendum)
    prev = f'chapter-{number-1:02d}.html'
    next_page = f'<a href="chapter-{number+1:02d}.html">Next chapter →</a>' if any(int(m.group(1)) == number + 1 for m in chapter_matches) else ''
    out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter {number} — {html.escape(title)} | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page chapter">{markdown.markdown(text, extensions=['extra','sane_lists'])}<section><h2>Media references</h2><div class="media-grid">{media_cards(relevant)}</div></section><nav class="chapter-nav"><a href="{prev}">← Previous chapter</a>{next_page}</nav></main><footer class="site-footer">Early Queer History · Chapter {number}</footer></body></html>'''
    Path(f'{slug(number, title)}.preview.html').write_text(out, encoding='utf-8')
def norm(url):
    return re.sub(r'/$', '', re.sub(r'[?#].*$', '', html.unescape(url).strip().lower()))
bib = (root / 'bibliography.html').read_text(encoding='utf-8')
existing = re.findall(r'<a[^>]+href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', bib, re.I|re.S)
entries = []
seen = set()
for url, label in existing:
    key = norm(url)
    if key not in seen:
        seen.add(key); entries.append((re.sub(r'<[^>]+>', '', label).strip() or url, url))
for filename, text in addendum_texts:
    for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', text):
        key = norm(url)
        if key not in seen:
            seen.add(key); entries.append((label.strip() or filename, url.strip()))
items = '\n'.join(f'<li><a href="{html.escape(url, quote=True)}">{html.escape(label)}</a></li>' for label, url in entries)
out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bibliography | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page"><h1>Bibliography</h1><p>Sources consolidated from the existing bibliography and repository addendums. Each normalized source URL appears once.</p><ol>{items}</ol></main><footer class="site-footer">Early Queer History</footer></body></html>'''
(root / 'bibliography.preview.html').write_text(out, encoding='utf-8')