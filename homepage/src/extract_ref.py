# -*- coding: utf-8 -*-
"""Extracts the reference site (prolifics-website.vercel.app, downloaded to ../ref/*.html on 22 Nov 2026) into
src/ref.json: per page the title, lead, hero bullets and an ordered list of sections with their headings,
paragraphs, cards (h3 + text + link), table rows, FAQ pairs and links. The page builders render from this."""
import os, json, re
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__)); REF = os.path.join(os.path.dirname(HERE), "ref")
T = lambda el: re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""

def clean(s):
    s = s.replace("–", ", ").replace("—", ", ").replace(" , ", ", ").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s*→\s*$", "", s).replace("→", "").strip()
    return re.sub(r"\s+", " ", s)

def section(sec):
    out = {"cls": " ".join(sec.get("class") or []), "h": clean(T(sec.find(["h1", "h2"]))), "eyebrow": "", "p": [], "cards": [], "table": [], "faq": [], "links": [], "li": []}
    eb = sec.find(class_=re.compile(r"eyebrow|kicker|label|tag"))
    if eb: out["eyebrow"] = clean(T(eb))
    for d in sec.find_all("details"):
        q = d.find("summary"); qt = clean(T(q)); 
        if q: q.extract()
        out["faq"].append((qt, clean(T(d))))
    for tr in sec.find_all("tr"):
        cells = [clean(T(c)) for c in tr.find_all(["th", "td"])]
        if cells: out["table"].append(cells)
    for h3 in sec.find_all("h3"):
        box = h3.parent
        while box is not sec and len(box.find_all("h3")) == 1 and box.parent is not sec and len(box.parent.find_all("h3")) == 1:
            box = box.parent
        ps = [clean(T(p)) for p in box.find_all("p")]
        a = box.find("a", href=True)
        num = box.find(class_=re.compile(r"num|step|index"))
        out["cards"].append({"t": clean(T(h3)), "d": " ".join(x for x in ps if x and x != clean(T(h3))), "href": a["href"] if a else "",
                             "a": clean(T(a)) if a else "", "n": clean(T(num)) if num else ""})
    out["boxes"] = []
    for c in sec.find_all("div", class_="card"):
        t = c.find(class_=re.compile(r"card__t"))
        if t and not c.find("h3"):
            n = c.find(class_="card__n"); d = c.find(class_="card__d"); a = c.find("a", href=True)
            out["cards"].append({"t": clean(T(t)), "d": clean(T(d)), "href": a["href"] if a else "", "a": clean(T(a)) if a else "", "n": clean(T(n))})
        elif c.find("p", class_="card__n"):
            head = c.find("p", class_="card__n")
            items = [clean(T(x)) for x in c.find_all("li")] or [clean(T(x)) for x in c.find_all("span")]
            out["boxes"].append({"t": clean(T(head)), "items": [x for x in items if x]})
    card_text = set(c["d"] for c in out["cards"]) | set(c["t"] for c in out["cards"])
    for p in sec.find_all("p"):
        if p.find_parent("details") or p.find_parent("table"): continue
        if any(p in c for c in []): pass
        t = clean(T(p))
        if t and t != out["eyebrow"] and not any(t and t in c for c in card_text):
            out["p"].append(t)
    for li in sec.find_all("li"):
        if li.find_parent("details"): continue
        t = clean(T(li))
        if t: out["li"].append(t)
    for a in sec.find_all("a", href=True):
        if a.find_parent("details"): continue
        out["links"].append((clean(T(a)), a["href"]))
    return out

def page(path):
    s = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    for x in s(["script", "style", "header", "footer", "nav"]): x.extract()
    m = s.find("main") or s.body
    secs = [section(x) for x in m.find_all("section") if not x.find_parent("section")]
    if not secs: secs = [section(m)]
    h1 = m.find("h1")
    meta = s.find("meta", attrs={"name": "description"})
    return {"title": clean(T(s.find("title"))).replace(" | Prolifics", ""), "h1": clean(T(h1)), "desc": meta["content"] if meta else "", "sections": secs}

if __name__ == "__main__":
    out = {}
    for f in sorted(os.listdir(REF)):
        if not f.endswith(".html"): continue
        key = "/" + f[:-5].replace("__", "/") if f != "home.html" else "/"
        out[key] = page(os.path.join(REF, f))
    json.dump(out, open(os.path.join(HERE, "ref.json"), "w"), indent=1, ensure_ascii=False)
    print(len(out), "pages")
