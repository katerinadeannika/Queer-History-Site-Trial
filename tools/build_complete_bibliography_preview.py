from pathlib import Path
import html, re
root = Path('.')
def norm(url):
    url = html.unescape(url).strip()
    url = re.sub(r'[?#].*$', '', url).rstrip('/').lower()
    return url
entries, seen = [], set()
def add(label, url):
    if not url.startswith(('http://', 'https://')):
        return
    key = norm(url)
    if key and key not in seen:
        seen.add(key)
        entries.append((re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(label))).strip() or url, url.strip()))
def html_links(text):
    return re.findall(r'<a[^>]+href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', text, re.I | re.S)
def markdown_links(text):
    return re.findall(r'\[([^\]]+)\]\((https?://[^)\s]+)(?:\s+[^)]*)?\)', text)
# Preserve established bibliography labels and ordering first.
bibliography = (root / 'bibliography.html').read_text(encoding='utf-8')
for url, label in html_links(bibliography):
    add(label, url)
# Add every linked source from the complete master document.
master = (root / 'Before_the_Name_complete_master.md').read_text(encoding='utf-8')
for label, url in markdown_links(master):
    add(label, url)
for url, label in html_links(master):
    add(label, url)
# Add every current chapter page, including any Chapter 12 file if present.
for page in sorted(root.glob('chapter-*.html')):
    text = page.read_text(encoding='utf-8')
    for url, label in html_links(text):
        add(label, url)
    for label, url in markdown_links(text):
        add(label, url)
# Add all Markdown addendums and appendices.
for source in sorted(root.glob('*.md')):
    if 'addendum' in source.name.lower() or 'appendix' in source.name.lower():
        text = source.read_text(encoding='utf-8')
        for label, url in markdown_links(text):
            add(label, url)
        for url, label in html_links(text):
            add(label, url)
items = '\n'.join(f'<li><a href="{html.escape(url, quote=True)}">{html.escape(label)}</a></li>' for label, url in entries)
out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bibliography | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page"><h1>Bibliography</h1><p>Consolidated sources from the complete master document, current chapter pages, existing bibliography, and repository addendums. Each normalized source URL appears once.</p><ol>{items}</ol></main><footer class="site-footer">Early Queer History</footer></body></html>'''
(root / 'bibliography.preview.html').write_text(out, encoding='utf-8')