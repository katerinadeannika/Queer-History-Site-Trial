from pathlib import Path
import html,re
MAIN='Before_the_Name_1880-1969.md'
ADDENDA=['Before_the_Name_image_links_appendix.md','audiovisual-reference-addendum-1880-1969.md','Before_the_Name_combined_addendum.md']
def linkify(s): return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<a href="{html.escape(m.group(2),quote=True)}">{html.escape(m.group(1))}</a>',html.escape(s))
def chapter_slice(text):
 a=text.index('## Chapter 2 — 1880–1889: Before the Name');b=text.index('## Chapter 3 — 1890–1899: The Trial That Named a World',a);return text[a:b].strip()
def addendum_slice(text):
 m=re.search(r'(?im)^#{1,6} .*?(?:chapter\s*2|1880[–-]1889|victorian)\b.*$',text)
 if not m:return ''
 n=re.search(r'(?m)^#{1,6} ',text[m.end():]);return text[m.start():m.end()+n.start()] if n else text[m.start():]
def media_cards(texts):
 seen=set();cards=[]
 for text in texts:
  for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)',text):
   url=url.strip()
   if url in seen:continue
   seen.add(url);low=url.lower().split('?')[0];title=html.escape(label);href=html.escape(url,quote=True)
   media=f'<img src="{href}" alt="{title}" loading="lazy">' if low.endswith(('.jpg','.jpeg','.png','.gif','.webp')) else f'<video controls preload="metadata"><source src="{href}"></video>' if low.endswith(('.mp4','.webm')) else f'<audio controls preload="metadata"><source src="{href}"></audio>' if low.endswith(('.mp3','.ogg','.wav')) else ''
   cards.append(f'<article class="media-reference">{media}<h3>{title}</h3><p><a href="{href}">Source, media reference, and rights note</a></p></article>')
 return '\n'.join(cards) or '<p>No chapter-specific external media references were found automatically; retain the chapter reference atlas as the source record.</p>'
src=Path(MAIN).read_text(encoding='utf-8');md=chapter_slice(src);lines=[];in_list=False
for raw in md.splitlines():
 s=raw.strip()
 if s.startswith('## '):lines.append(f'<h1>{linkify(s[3:])}</h1>')
 elif s.startswith('### '):
  if in_list:lines.append('</ul>');in_list=False
  lines.append(f'<h2>{linkify(s[4:])}</h2>')
 elif s.startswith('- '):
  if not in_list:lines.append('<ul>');in_list=True
  lines.append(f'<li>{linkify(s[2:])}</li>')
 elif s.startswith('> '):
  if in_list:lines.append('</ul>');in_list=False
  lines.append(f'<blockquote>{linkify(s[2:])}</blockquote>')
 elif s and not s.startswith('<a ') and not s.startswith('---'):
  if in_list:lines.append('</ul>');in_list=False
  lines.append(f'<p>{linkify(s)}</p>')
if in_list:lines.append('</ul>')
adds=[addendum_slice(Path(p).read_text(encoding='utf-8')) for p in ADDENDA];media=media_cards([md,*adds])
out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 2 — 1880–1889: Before the Name</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page chapter"><p class="eyebrow">Editorial preview · verbatim canonical chapter text</p>{''.join(lines)}<section><h2>Media references</h2><p>Direct image, audio, and video files are embedded when their URL identifies a media file. Archive and discovery pages remain linked cards rather than being represented as hosted media.</p><div class="media-grid">{media}</div></section></main><footer class="site-footer">Editorial preview — not deployed</footer></body></html>'''
Path('chapter-02-1880s.preview.html').write_text(out,encoding='utf-8')