#!/usr/bin/env python3
import html, re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path('.'); BIB=ROOT/'bibliography.html'; BACKUP=ROOT/'backup-sources.html'
START='<!-- AUTO-SOURCE-INVENTORY:START -->'; END='<!-- AUTO-SOURCE-INVENTORY:END -->'
BSTART='<!-- AUTO-REMOVED-SOURCES:START -->'; BEND='<!-- AUTO-REMOVED-SOURCES:END -->'
TAG=re.compile(r'''(?is)<(?P<tag>a|img|audio|video|source|iframe|embed|object)\b(?P<attrs>[^>]*)>''')
ATTR=re.compile(r'''(?is)\b(?P<n>href|src|poster|data|cite|data-source|data-citation)\s*=\s*["'](?P<v>[^"']+)["']''')
URL=re.compile(r'''(?ix)\b(?:https?://|www\.|doi:\s*10\.)[^\s<>"']+''')
ITEM=re.compile(r'''(?is)<li\s+data-source-key=["'](?P<k>[^"']+)["']>(?P<b>.*?)</li>''')
KIND={'a':'External link or citation','img':'Image','audio':'Audio or radio','video':'Video','source':'Media source','iframe':'Embedded content','embed':'Embedded content','object':'Embedded content'}
TRAIL='.,;:!?)]}\"\''

def external(v):
    v=html.unescape(v).strip(); return urlparse(v).scheme in {'http','https'} or v.lower().startswith('www.') or v.lower().startswith('doi:')
def local_media(v):
    v=html.unescape(v).strip(); return bool(v and not v.startswith(('#','mailto:','tel:','javascript:','data:')))
def ensure(text,a,b):
    if a in text and b in text:return text
    if '</main>' in text:return text.replace('</main>',a+'\n'+b+'\n</main>',1)
    return text+'\n'+a+'\n'+b+'\n'
def between(text,a,b):
    i,j=text.find(a),text.find(b)
    if i<0 or j<i: raise SystemExit('Inventory markers unavailable')
    return text[i+len(a):j]
def replace(text,a,b,body):
    i,j=text.find(a),text.find(b); return text[:i+len(a)]+'\n'+body+'\n'+text[j:]
def collect():
    out={}
    def add(kind,v,page):
        v=html.unescape(v).strip().rstrip(TRAIL); k=kind+'|'+v
        out.setdefault(k,{'kind':kind,'value':v,'pages':set()})['pages'].add(page)
    for p in sorted(ROOT.glob('*.htm*')):
        if p.name in {BIB.name,BACKUP.name}:continue
        t=p.read_text(encoding='utf-8')
        for m in TAG.finditer(t):
            tag=m['tag'].lower()
            for x in ATTR.finditer(m['attrs']):
                n,v=x['n'].lower(),x['v']
                if (tag=='a' and n=='href' and external(v)) or (tag!='a' and external(v)) or (tag in {'img','audio','video','source'} and n in {'src','poster'} and local_media(v)): add(KIND[tag],v,p.name)
        for v in URL.findall(t):
            if external(v):add('In-text URL or DOI',v,p.name)
    return out
def parse(t): return {html.unescape(m['k']):m['b'] for m in ITEM.finditer(t)}
def entry(k,e):
    v=html.escape(e['value'],quote=True); pages=', '.join(html.escape(x) for x in sorted(e['pages']))
    target=f'<a href="{v}">{v}</a>' if external(e['value']) else f'<code>{v}</code>'
    return f'<li data-source-key="{html.escape(k,quote=True)}"><strong>{html.escape(e["kind"])}</strong>: {target} <em>Referenced in: {pages}</em></li>'
def render(entries,title):
    g=defaultdict(list)
    for k,e in entries.items():g[e['kind']].append((k,e))
    lines=[f'<section id="automated-source-inventory"><h2>{title}</h2>','<p>This generated section inventories references found on current site pages. Edit the page reference rather than this list.</p>']
    for kind in sorted(g):lines += [f'<h3>{html.escape(kind)}</h3>','<ul>']+[entry(k,e) for k,e in sorted(g[k],key=lambda x:x[1]['value'].lower())]+['</ul>']
    return '\n'.join(lines+['</section>'])
def main():
    active=collect(); text=ensure(BIB.read_text(encoding='utf-8'),START,END); old=parse(between(text,START,END)); BIB.write_text(replace(text,START,END,render(active,'Automatically generated source inventory')),encoding='utf-8')
    if BACKUP.exists():bt=BACKUP.read_text(encoding='utf-8')
    else:bt='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Backup Sources</title></head><body><main><h1>Backup sources</h1><p>References removed from the active automatic bibliography are retained here.</p>'+BSTART+BEND+'</main></body></html>\n'
    bt=ensure(bt,BSTART,BEND); saved=parse(between(bt,BSTART,BEND)); saved.update({k:v for k,v in old.items() if k not in active})
    body='<section id="removed-source-inventory"><h2>Removed sources</h2><p>Retained automatically with their original links and last-known page references.</p><ul>'+''.join(f'<li data-source-key="{html.escape(k,quote=True)}">{v}</li>' for k,v in sorted(saved.items()))+'</ul></section>'
    BACKUP.write_text(replace(bt,BSTART,BEND,body),encoding='utf-8')
if __name__=='__main__':main()
