import html,json,sys
from pathlib import Path

def card(x):
    image=f'<img src="{html.escape(x["image"])}" alt="{html.escape(x["alt"])}">' if x.get("image") else ''
    return f'<figure class="media-card">{image}<figcaption><strong>{html.escape(x["title"])}</strong><br>{x["caption"]}<br><a class="source" href="{html.escape(x["source"])}">Source and citation</a></figcaption></figure>'

def media(x):
    return f'<article class="media-reference"><h3>{html.escape(x["title"])}</h3><p>{x["caption"]}</p><p><a href="{html.escape(x["source"])}">Source and citation</a></p></article>'

def main():
    d=json.load(open(sys.argv[1],encoding="utf-8"))
    text=''.join(f'<section><h2>{html.escape(s["heading"])}</h2>{s["html"]}</section>' for s in d["sections"])
    images=''.join(card(x) for x in d["images"])
    av=''.join(media(x) for x in d["audiovisual"])
    notes=''.join(f'<li>{n}</li>' for n in d["notes"])
    out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter {d["number"]} — {d["title"]} | Early Queer History</title><link rel="stylesheet" href="site.css"></head><body><header class="site-header"><a href="index.html">Home</a><a href="chapters.html">Chapters</a><a href="research.html">Research</a><a href="bibliography.html">Bibliography</a></header><main class="page"><p class="eyebrow">Before the Name · {d["years"]}</p><h1>Chapter {d["number"]} — {d["title"]}</h1><p class="lede">{d["lede"]}</p>{text}<section><h2>Visual reference gallery</h2><div class="media-grid">{images}</div></section><section><h2>Audio and video references</h2>{av}</section><section class="notes"><h2>Notes and sources</h2><ol>{notes}</ol></section><nav class="chapter-nav"><a href="{d["previous"]}">← Previous chapter</a><a href="{d["next"]}">Next chapter →</a></nav></main><footer class="site-footer">Early Queer History · Chapter {d["number"]}</footer></body></html>'''
    Path(d["output"]).write_text(out,encoding="utf-8")
if __name__=="__main__": main()
