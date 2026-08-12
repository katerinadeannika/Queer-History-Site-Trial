# Retry trigger: force a fresh Chapter 2 editorial render.
from pathlib import Path
import html,re,markdown
MAIN='Before_the_Name_1880-1969.md'
ADDENDA=['Before_the_Name_image_links_appendix.md','audiovisual-reference-addendum-1880-1969.md','Before_the_Name_combined_addendum.md']
def chapter_slice(t):
 a=t.index('## Chapter 2 — 1880–1889: Before the Name');b=t.index('## Chapter 3 — 1890–1899: The Trial That Named a World',a);return t[a:b].strip()
def relevant(t):
 m=re.search(r'(?im)^#{1,6} .*?(?:chapter\s*2|1880[–-]1889|victorian)\b.*$',t)
 if not m:return ''
 n=re.search(r'(?m)^#{1,6} ',t[m.end():]);return t[m.start():m.end()+n.start()] if n else t[m.start():]
def cards(ts):
 seen=set();o=[]
 for t in ts:
  for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)',t):
   if url in seen:continue
   seen.add(url);low=url.lower().split('?')[0];title=html.escape(label);href=html.escape(url,quote=True)
   media=f'<img src="{href}" alt="{title}" loading="lazy">' if low.endswith(('.jpg','.jpeg','.png','.gif','.webp')) else f'<video controls preload="metadata"><source src="{href}"></video>' if low.endswith(('.mp4','.webm')) else f'<audio controls preload="metadata"><source src="{href}"></audio>' if low.endswith(('.mp3','.ogg','.wav')) else ''
   o.append(f'<article class="media-reference">{media}<h3>{title}</h3><p><a href="{href}">Source, media reference, and rights note</a></p></article>')
 return ''.join(o)
chapter=chapter_slice(Path(MAIN).read_text(encoding='utf-8'));content=markdown.markdown(chapter,extensions=['extra','sane_lists']);media=cards([chapter,*[relevant(Path(x).read_text(encoding='utf-8')) for x in ADDENDA]])
out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 2 — 1880–1889: Before the Name | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page chapter">{content}<section><h2>Media references</h2><p>Direct media files are embedded when available; archive and discovery sources remain linked with item-level rights notes.</p><div class="media-grid">{media}</div></section><nav class="chapter-nav"><a href="chapter-01-introduction.html">← Previous chapter</a><a href="chapter-03-1890s.html">Next chapter →</a></nav></main><footer class="site-footer">Early Queer History · Chapter 2</footer></body></html>'''
Path('chapter-02-1880s.preview.html').write_text(out,encoding='utf-8')