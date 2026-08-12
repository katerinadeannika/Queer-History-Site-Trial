from pathlib import Path
import html,re

src=Path('Before_the_Name_1880-1969.md').read_text(encoding='utf-8')
start=src.index('## Chapter 2 — 1880–1889: Before the Name')
end=src.index('## Chapter 3 — 1890–1899: The Trial That Named a World',start)
md=src[start:end].strip()
lines=[]
in_list=False
for raw in md.splitlines():
    s=raw.strip()
    if s.startswith('## '):
        lines.append(f'<h1>{html.escape(s[3:])}</h1>')
    elif s.startswith('### '):
        if in_list: lines.append('</ul>'); in_list=False
        lines.append(f'<h2>{html.escape(s[4:])}</h2>')
    elif s.startswith('- '):
        if not in_list: lines.append('<ul>'); in_list=True
        lines.append(f'<li>{html.escape(s[2:])}</li>')
    elif s.startswith('> '):
        if in_list: lines.append('</ul>'); in_list=False
        lines.append(f'<blockquote>{html.escape(s[2:])}</blockquote>')
    elif s and not s.startswith('<a ') and not s.startswith('---'):
        if in_list: lines.append('</ul>'); in_list=False
        lines.append(f'<p>{html.escape(s)}</p>')
if in_list: lines.append('</ul>')
body='\n'.join(lines)
out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 2 — 1880–1889: Before the Name</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page chapter"><p class="eyebrow">Editorial preview · extracted verbatim from the canonical manuscript</p>{body}<section><h2>Media references</h2><p>Chapter-specific external media cards will be inserted from the complete master’s mapped addendum entries after editorial review. Source links remain subject to item-level rights and embedding checks.</p></section></main><footer class="site-footer">Editorial preview — not deployed</footer></body></html>'''
Path('chapter-02-1880s.preview.html').write_text(out,encoding='utf-8')
