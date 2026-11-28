# -*- coding: utf-8 -*-
"""Builds the whole site (22 Nov 2026, Mac: "build the rest") into ../dist after build_home.py.
   python3 src/build_home.py && python3 src/build_site.py        (add --final to drop noindex)
Every page of the reference site (prolifics-website.vercel.app/sitemap.xml, 109 URLs) is rebuilt in the approved
consulting style. Copy comes from src/ref.json (extracted by extract_ref.py), enhanced only with sourced material:
company figures and group firms (content.py), Salesforce GTM content (sf_data.json) and published case studies
(cases.py). The five pages Mac reviewed keep their own builders in build_pages.py."""
import os, re, json, sys, shutil
from PIL import Image
import build_pages as P
from build_pages import H, E, arrow, img, icon, crumbs, ctas, subnav, sec, steps, table, faq, example, related, band, contact, engage, sprint, logo, shell
from content import *
from pages_content import *
from cases import LIB, PRACTICE_CASES, INDUSTRY_CASES
from optimize import optimize
from logoutil import prep

HERE, DIST = H.HERE, H.DIST
REF = json.load(open(os.path.join(HERE, "ref.json"), encoding="utf-8"))
PR = {p["k"]: p for p in PRACTICES}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "s"

# ---------------------------------------------------------------- lookups
SVC = {}          # href -> (practice key, group name, service name)
for p in PRACTICES:
    for g, links in p["groups"]:
        for t, u in links:
            if u not in SVC and u != p["href"]: SVC[u] = (p["k"], g, t)
SVC["/services/cloud"] = ("app", "Cloud & Infrastructure", "Cloud")
SVC["/services/data-ai"] = ("ai", "Data", "Data & AI")
PRACTICE_PATH = {p["href"]: p["k"] for p in PRACTICES}
SOL = {}
for g, items in SOLUTIONS:
    for t, d, u, ic, tl in items: SOL[u] = dict(group=g, title=t, desc=d, url=u, icon=ic, tl=tl)
for txt, u in REF["/solutions"]["sections"][1]["links"]:
    m = re.search(r"Timeline (.*?) First step (.*)$", txt)
    if m and u in SOL:
        SOL[u]["tl"] = re.sub(r"(\d), (\d)", r"\1 to \2", m.group(1)); SOL[u]["first"] = m.group(2)
for i, u in enumerate(SOL): SOL[u]["img"] = SOL_CARD_IMG[i]
FIRM = {"sf": "Enable Consulting, a Salesforce partner since 2002", "sap": "Castaliaz, an SAP Gold Partner", "qe": "Prolifics Testing"}
POD = {"ai": "AI & Data Pod", "sf": "Salesforce & Agentforce Pod", "sn": "ServiceNow Pod", "sap": "SAP & ERP Pod", "app": "Integration & Automation Pod", "qe": "Quality & Testing for AI Pod"}
GUIDE_LINKS = [(t, d, u) for t, d, u, im in GUIDES]
STD_FAQ = [
    ("How does an engagement start?", "With one defined process, its data, its owners and a measure the business signs off. Discovery confirms dependencies and entitlements before we commit to scope or dates."),
    ("How are results measured?", "We record a baseline before release and compare like for like work afterward with your process owners. Targets are agreed with you, not promised in advance."),
    ("Which engagement models are available?", "Advisory, co-delivery, build-operate-transfer or fully managed. The choice depends on who should own the result in production and how quickly your team needs to take over."),
]

# ---------------------------------------------------------------- generic section renderer
STEP_WORDS = re.compile(r"\b(path|approach|how it works|journey|move from|delivery path|steps|how a|roadmap)\b", re.I)
SKIP_EB = ("related solutions", "related services", "more in", "more solutions")
SKIP_H = ("bring us", "start with a business", "explore related", "discuss your", "talk to", "explore prolifics", "learn about the team")

def blocks(page, skip_hero=True):
    out = []
    secs = page["sections"][1:] if skip_hero else page["sections"]
    for s in secs:
        h, eb = s["h"], s["eyebrow"]
        if not h and s["boxes"]: h = "What you get"
        if not h or eb.lower().startswith(SKIP_EB) or h.lower().startswith(SKIP_H): continue
        intro = " ".join(x for x in s["p"] if len(x) > 40)
        kind, html = None, ""
        if s["faq"]:
            kind, html = "faq", faq(s["faq"])
        elif s["table"]:
            head, rows = s["table"][0], s["table"][1:]
            kind, html = "table", table([(r[0], r[1]) for r in rows if len(r) > 1], (head[0], head[1]) if len(head) > 1 else ("Measure", "What to assess"))
            if intro: html += '<p class="note">%s</p>' % E(intro)
            intro = ""
        elif s["cards"]:
            cards = s["cards"]
            if not any(c["href"] for c in cards) and STEP_WORDS.search(h) and len(cards) <= 6:
                kind, html = "steps", steps([(c["t"], c["d"]) for c in cards])
            else:
                kind, html = "caps", P.caps([(c["t"], c["d"], c["href"] if c["href"].startswith("/") and not c["href"].startswith("/solutions") else None) for c in cards])
        elif s["boxes"]:
            kind = "boxes"
            html = '<div class="bx3">%s</div>' % "".join('<div class="bx" data-r><p class="bx-h">%s</p><ul>%s</ul></div>' % (E(b["t"]), "".join("<li>%s</li>" % E(i) for i in b["items"])) for b in s["boxes"])
        elif s["p"]:
            if h.lower().startswith("example"):
                kind, html = "example", ('<aside class="ex" data-r><p class="ex-k">Illustrative delivery scenario</p><p>%s</p></aside>' % E(" ".join(s["p"])))
            else:
                kind, html = "text", "".join('<p class="big-p">%s</p>' % E(x) for x in s["p"])
            intro = ""
        elif s["li"]:
            kind, html = "list", '<ul class="chk">%s</ul>' % "".join('<li>%s%s</li>' % (icon("check", 20), E(x)) for x in s["li"])
        if not kind: continue
        hl = h.lower()
        label = {"faq": "FAQ", "table": "Measures", "steps": "Approach", "example": "Example", "boxes": "Outcomes"}.get(kind)
        if not label:
            if kind == "caps" and not any(b["kind"] == "caps" for b in out): label = "Capabilities"
            elif hl.startswith("who"): label = "Who it is for"
            elif hl.startswith("what to bring") or hl.startswith("prepare"): label = "What to bring"
            elif hl.startswith("why"): label = "Why it matters"
            else: label = short(h)
        default_eb = {"caps": "What we deliver", "steps": "Approach", "text": "Overview", "list": "Checklist", "boxes": "Outcomes", "table": "Measures", "faq": "FAQ", "example": "Example"}[kind]
        if kind == "text" and hl.startswith("who"): default_eb = "Who it is for"
        good_eb = eb and not eb.lower().startswith(("delivered", "draft")) and eb.lower() not in ("industries", "esg vision", "social impact")
        out.append(dict(id=slug(label), label=label, eyebrow=eb if good_eb else default_eb, h=h, intro=intro if kind != "text" else "", html=html, kind=kind))
    seen = set()
    for b in out:
        while b["id"] in seen: b["id"] += "-2"
        seen.add(b["id"])
    return out

def short(h):
    h = re.sub(r":.*$", "", h)
    w = h.split()
    return " ".join(w[:3]) if len(w) > 3 else h

def lead_of(page):
    ps = page["sections"][0]["p"] if page["sections"] else []
    return next((x for x in ps if len(x) > 50), ps[-1] if ps else "")

def case_grid(keys, n=6):
    cards = []
    for k in keys[:n]:
        c = LIB[k]
        head = logo(c["logo"], "cc-lg") if c["logo"] else '<span class="cc-cl">%s</span>' % E(c["client"])
        met = '<span class="cc-m"><b>%s</b><span>%s</span></span>' % (E(c["m"]), E(c["ml"])) if c["m"] and c["m"] not in P.WEAK else ""
        cards.append('<a class="cc sw" href="%s" rel="noopener" data-r><span class="cc-im">%s<span class="chip-i">%s</span></span><span class="cc-b">%s%s'
                     '<span class="cc-t">%s</span><span class="cc-d">%s</span><span class="cc-f"><span>Delivered by %s</span></span>'
                     '<span class="cc-x">Read the case study %s</span></span></a>' % (c["url"], img(c["im"], ""), E(c["sector"]), head, met, E(c["title"]), E(c["brief"]), E(c["by"]), arrow()))
    return '<div class="ccs">%s</div>' % "".join(cards)

def stack(id_, eyebrow, title, intro, body, cls=""):
    return sec(id_, eyebrow, title, body, intro, ("stack " + cls).strip())

def sol_cards(urls):
    return '<div class="slc">%s</div>' % "".join(
        '<a class="sl" href="%s" data-r><span class="sl-im">%s</span><span class="sl-b"><span class="sl-g">%s</span><b>%s</b><span class="sl-d">%s</span>'
        '<span class="sl-f"><span>%s</span><span class="sl-x">Explore %s</span></span></span></a>'
        % (u, img(SOL[u]["img"], ""), E(SOL[u]["group"]), E(SOL[u]["title"]), E(SOL[u]["desc"]), E(SOL[u].get("tl") or "Scoped on discovery"), arrow()) for u in urls if u in SOL)

def ind_tiles(cls="g4"):
    return '<ul class="sig %s">%s</ul>' % (cls, "".join(
        '<li class="si" data-r><a class="si-a" href="%s">%s<span class="si-sh"></span><span class="si-b"><span class="si-ic">%s</span><b>%s</b><span class="si-d">%s</span>'
        '<span class="si-p"><small>Explore</small>%s %s</span></span></a></li>' % (u, img(im, ""), icon(ic, 22), E(t), E(d), E(t), arrow()) for t, d, u, ic, im in INDUSTRIES))

def kf_panel(rows):
    return '<aside class="kf" aria-label="At a glance"><p class="side-h">At a glance</p><dl>%s</dl></aside>' % "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(a), b) for a, b in rows if b)

def link(t, u): return '<a href="%s">%s</a>' % (u, E(t))

def bands_from(blks, alt_start=False):
    html, i = "", 0
    for b in blks:
        cls = "alt" if (i % 2 == 1) != alt_start else ""
        if b["kind"] in ("caps",) and len(b["html"]) > 0 and "stack" in b.get("cls", ""): pass
        html += sec(b["id"], b["eyebrow"], b["h"], b["html"], b["intro"], cls); i += 1
    return html

# ---------------------------------------------------------------- practice pages
PRACTICE_HERO = {
    "ai": [("Since 2015", "Information management and analytics through Stream Integration"), ("2,000+", "engineers, architects and consultants across the group")],
    "fde": [("6 weeks", "from a signed baseline to one AI workflow in production"), ("6 pods", "AI and data, Salesforce, ServiceNow, SAP, integration and quality")],
    "sn": [("10 services", "across the AI platform, workflows, build and run"), ("48 years", "of integration and automation work behind every workflow")],
    "sap": [("Castaliaz", "SAP Gold Partner, part of Prolifics since 2025"), ("99%+", "defect removal efficiency on an SAP S/4HANA migration for McKesson")],
    "app": [("680+", "point to point interfaces rationalized for RAC"), ("50%", "annual cost reduction reported by The Insolvency Service")],
    "bt": [("60M", "claims a year through automated handling at Horizon BCBSNJ"), ("Under 10 days", "court claims processing in Tennessee, down from 45")],
    "qe": [("Since 2017", "e-testing joins, now part of Prolifics Testing"), ("99%+", "defect removal efficiency on McKesson's SAP S/4HANA migration")],
}
PRACTICE_SOL = {"ai": ["/solutions/agentic-starter", "/solutions/knowledge-assistant", "/solutions/data-platform"],
                "fde": ["/solutions/agentic-starter", "/solutions/ai-governance", "/solutions/process-agents"],
                "sn": ["/solutions/service-desk", "/solutions/ai-governance", "/solutions/process-agents"],
                "sap": ["/solutions/s4-fasttrack", "/solutions/ai-testing", "/solutions/legacy-ai"],
                "app": ["/solutions/legacy-ai", "/solutions/process-agents", "/solutions/idp"],
                "bt": ["/solutions/process-agents", "/solutions/idp", "/solutions/agentic-starter"],
                "qe": ["/solutions/ai-testing", "/solutions/eu-ai-act", "/solutions/ai-governance"]}

def practice_hero(k, page):
    p = PR[k]; c1, c2 = PRACTICE_HERO[k]
    tags = "".join("<li>%s</li>" % E(g) for g, l in p["groups"])
    return ('<section class="ph sfh"><div class="wrap ph-in"><div class="ph-t"><p class="kick">%s practice</p><h1>%s</h1><p class="ph-lead">%s</p>%s<ul class="sfh-tags">%s</ul></div>'
            '<figure class="ph-fig sfh-fig">%s<figcaption class="fl fl1"><b>%s</b><span>%s</span></figcaption><figcaption class="fl fl2"><b>%s</b><span>%s</span></figcaption></figure></div></section>'
            % (E(p["name"]), E(page["h1"]), E(lead_of(page)), ctas(second=("Explore %s services" % p["name"], "#services")), tags, img(p["img"], "", "", True), E(c1[0]), E(c1[1]), E(c2[0]), E(c2[1])))

def explorer_for(k):
    p = PR[k]; tabs, panels, seen, i = [], [], set(), 0
    for g, links in p["groups"]:
        for t, u in links:
            if u in seen or u == p["href"] or u not in REF: continue
            seen.add(u); pg = REF[u]
            caps_ = [c["t"] for s in pg["sections"] for c in s["cards"]][:4]
            sid = slug(u.rsplit("/", 1)[-1]); sel = i == 0
            tabs.append('<button type="button" class="cx-t" role="tab" id="cxt-%s" aria-controls="cxp-%s" aria-selected="%s" tabindex="%d"><span class="cx-n">%02d</span><span class="cx-l"><b>%s</b><small>%s</small></span></button>'
                        % (sid, sid, "true" if sel else "false", 0 if sel else -1, i + 1, E(t), E(g)))
            scope = "".join("<li>%s%s</li>" % (icon("check", 18), E(x)) for x in caps_)
            panels.append('<div class="cx-p" role="tabpanel" id="cxp-%s" aria-labelledby="cxt-%s"%s><div class="cx-ph"><span class="cx-ic">%s</span><div><p class="cx-k">%s</p><h3>%s</h3></div></div>'
                          '<p class="cx-s">%s</p>%s<a class="btn btn-p sm" href="%s">Explore %s %s</a></div>'
                          % (sid, sid, "" if sel else " hidden", icon(p["icon"], 30), E(g), E(t), E(lead_of(pg)),
                             ('<p class="cx-h">What is in scope</p><ul class="cx-sc">%s</ul>' % scope) if scope else "", u, E(t), arrow()))
            i += 1
    return i, '<div class="cx" data-r><div class="cx-tl" role="tablist" aria-label="%s services">%s</div><div class="cx-ps">%s</div></div>' % (E(p["name"]), "".join(tabs), "".join(panels))

def practice_page(k):
    p = PR[k]; page = REF[p["href"]]
    blks = blocks(page)
    faq_b = [b for b in blks if b["kind"] == "faq"]; blks = [b for b in blks if b["kind"] != "faq"]
    nav = [("clients", "Clients")] + [(b["id"], b["label"]) for b in blks[:3]]
    body = practice_hero(k, page)
    rest = H.logo_grid(P.GRID_LOGOS, P.ASPECT, "Selected clients across the Prolifics group", "clients")
    rest += bands_from(blks)
    if k == "fde":
        pods = "".join('<li data-r><span class="cap-n">%02d</span><h3>%s</h3><p>A forward deployed pod for %s work, with an onshore lead, a deployment strategist, an evaluation engineer and an engineering squad.</p></li>'
                       % (i + 1, E(t), E(t.replace(" Pod", "").replace("&", "and"))) for i, (t, u) in enumerate(p["groups"][0][1]))
        rest += stack("services", "Six pods", "One pod for each platform an AI workflow has to reach", "Small and senior, embedded with the business owner, accountable for one result in production.", '<ol class="caps">%s</ol>' % pods)
        rest += '<section class="ps alt" id="sprint"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">How a sprint runs</p><h2>Six weeks, four moves, one workflow in production</h2></header>%s</div></section>' % sprint()
        nav += [("services", "Pods"), ("sprint", "Sprint")]
    else:
        n, ex = explorer_for(k)
        rest += ('<section class="ps" id="services"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Services</p><h2>%d %s services, one delivery standard</h2>'
                 '<p class="ps-p">Choose a service to see what it covers, then open its page for the full approach.</p></header>%s</div></section>' % (n, E(p["name"]), ex))
        nav += [("services", "Services")]
    rest += ('<section class="ps alt" id="industries"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Industries we serve</p>'
             '<h2>Applied in the industries where Prolifics has delivered for decades</h2></header>%s</div></section>' % ind_tiles())
    nav += [("industries", "Industries")]
    cases = PRACTICE_CASES.get(k) or []
    if cases:
        rest += stack("work", "Selected work", "Published results from the %s practice" % p["name"], "Each card links to the published case study.", case_grid(cases))
        nav += [("work", "Work")]
    pod = ('<a class="pod" href="/services/fde-ai-engineering" data-r>%s<span><b>%s</b><span>A forward deployed pod embeds with your business owner and ships one workflow at a time.</span></span>%s</a>' % (icon("pod", 28), E(POD[k]), arrow())) if k in POD else ""
    rest += sec("engage", "Ways to engage", "Advisory, co-delivery, build-operate-transfer or fully managed", engage() + pod, "", "alt" if cases else "")
    if faq_b:
        b = faq_b[0]; rest += sec("faq", "FAQ", b["h"], b["html"]); nav += [("faq", "FAQ")]
    rest += '<section class="ps"><div class="wrap">%s</div></section>' % related(GUIDE_LINKS + [("All services", "Eight practices, grouped by the outcome you need.", "/services")], "Planning guides and more")
    rest += contact("Bring us one %s priority to discuss" % p["name"], "Share the process, systems and outcome you have in mind. We will discuss the dependencies, scope and the right next step with your team.")
    body += subnav(nav[:8], (p["start"][0], p["start"][1])) + rest
    return shell(page["title"] or p["name"], page["desc"] or p["long"], body, [("Home", "/"), ("Services", "/services"), (p["name"], None)])

# ---------------------------------------------------------------- service detail pages
def service_page(u):
    k, g, name = SVC[u]; p = PR[k]; page = REF[u]
    blks = blocks(page)
    kinds = {b["kind"] for b in blks}
    if "steps" not in kinds:
        blks.append(dict(id="approach", label="Approach", eyebrow="How we deliver", h="Scoped first, measured always", intro="", html=steps([(t, d) for w, t, d in SPRINT]), kind="steps"))
    sols = [x for t, x in next((s["links"] for s in page["sections"] if s["eyebrow"].lower().startswith("related solutions")), []) if x in SOL]
    cases = PRACTICE_CASES.get(k) or []
    if cases:
        rot = sum(map(ord, u)) % len(cases); cases = (cases[rot:] + cases[:rot])[:2]
    if "faq" not in kinds:
        blks.append(dict(id="faq", label="FAQ", eyebrow="FAQ", h="%s: frequently asked questions" % name, intro="", html=faq(STD_FAQ), kind="faq"))
    toc = [(b["id"], b["label"]) for b in blks] + ([("work", "Selected work")] if cases else [])
    sib = "".join('<li><p>%s</p><ul>%s</ul></li>' % (E(gg), "".join('<li><a href="%s"%s>%s</a></li>' % (x, ' aria-current="page"' if x == u else "", E(t)) for t, x in links if x != p["href"]))
                  for gg, links in p["groups"] if any(x != p["href"] for t, x in links))
    aside = ('<aside class="side"><nav class="toc" aria-label="On this page"><p class="side-h">On this page</p><ul>%s</ul></nav>'
             '<nav class="sibs" aria-label="%s services"><p class="side-h">%s services</p><ul>%s</ul></nav>'
             '<a class="side-cta" href="/contact"><b>Talk to an expert</b><span>Discuss %s %s</span></a></aside>'
             % ("".join('<li><a href="#%s">%s</a></li>' % (a, E(t)) for a, t in toc), E(p["name"]), E(p["name"]), sib, E(name), arrow()))
    dbl = lambda b: '<section class="dblk" id="%s"><p class="eyebrow">%s</p><h2>%s</h2>%s%s</section>' % (b["id"], E(b["eyebrow"]), E(b["h"]), ('<p class="ps-p blk-p">%s</p>' % E(b["intro"])) if b["intro"] else "", b["html"])
    content = "".join(dbl(b) for b in blks if b["kind"] != "faq")
    content += '<section class="dblk" id="engage"><p class="eyebrow">Ways to engage</p><h2>Choose who owns the result</h2>%s</section>' % engage()
    if cases:
        content += '<section class="dblk" id="work"><p class="eyebrow">Selected work</p><h2>Published results from the %s practice</h2>%s</section>' % (E(p["name"]), case_grid(cases, 2).replace('class="ccs"', 'class="ccs two"'))
    content += "".join(dbl(b) for b in blks if b["kind"] == "faq")
    rel = [("%s overview" % p["name"], p["desc"], p["href"])] + GUIDE_LINKS[:2]
    content += related(rel[:3], "Related services and guides")
    kfrows = [("Practice", link(p["name"], p["href"])), ("Service group", E(g)), ("Delivered with", E(FIRM[k]) if k in FIRM else ""),
              ("Ways to engage", "Advisory, co-delivery, build-operate-transfer, fully managed"),
              ("Forward deployed option", link(POD[k], "/services/fde-ai-engineering") if k in POD else ""),
              ("Start with", link(p["start"][0], p["start"][1]))]
    hero = ('<section class="ph slim"><div class="wrap ph-in"><div class="ph-t"><p class="kick">%s</p><h1>%s</h1><p class="ph-lead">%s</p>%s</div>%s</div></section>'
            % (E(name), E(page["h1"]), E(lead_of(page)), ctas(("Discuss %s" % name, "/contact"), ("See the approach", "#approach")), kf_panel(kfrows)))
    body = hero + '<div class="detail"><div class="wrap det-in">%s<div class="det-c">%s</div></div></div>' % (aside, content) + contact(
        "Bring us one workflow to discuss", "Share the process, systems and outcome you have in mind. We will discuss the dependencies, scope and the right next step with your team.")
    return shell(page["title"] or name, page["desc"] or lead_of(page), body, [("Home", "/"), ("Services", "/services"), (p["name"], p["href"]), (name, None)])

# ---------------------------------------------------------------- solutions
def solutions_landing():
    groups = [g for g, it in SOLUTIONS]
    chips = ['<button type="button" class="fc2 on" data-f="all" aria-pressed="true">All %d</button>' % len(SOL)] + [
        '<button type="button" class="fc2" data-f="%s" aria-pressed="false">%s</button>' % (slug(g), E(g)) for g in groups]
    cards = "".join(sol_cards([u]).replace('<a class="sl"', '<a class="sl" data-g="%s"' % slug(SOL[u]["group"]))[len('<div class="slc">'):-len("</div>")] for u in SOL)
    page = REF["/solutions"]
    body = (P.hero("Solutions", page["h1"], lead_of(page), "r06", ("16", "packaged solutions, each with a defined scope, timeline and first step"), ("How every solution runs", "#how"))
            + subnav([("all", "All solutions"), ("how", "How they run"), ("engage", "Ways to engage")], ("Talk to Our Experts", "/contact"))
            + '<section class="ps" id="all"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">All solutions</p><h2>Solve a specific business problem with a defined first step</h2>'
              '<p class="ps-p">Filter by the outcome you need. Each solution names its timeline and the first step that starts it.</p></header>'
              '<div class="fcs2" role="group" aria-label="Filter solutions">%s</div><div class="slc" id="sol-list">%s</div></div></section>' % ("".join(chips), cards)
            + stack("how", "How every solution runs", "Scoped first, measured always", "Every solution follows the same delivery standard as our practices.", steps([(t, d) for w, t, d in SPRINT]), "alt")
            + sec("engage", "Ways to engage", "Advisory, co-delivery, build-operate-transfer or fully managed", engage())
            + contact("Not sure which solution fits?", "Tell us the process and the result you need. We will point you to the right starting point, or scope a new one."))
    return shell("Solutions", page["desc"] or "Prolifics packaged solutions", body, [("Home", "/"), ("Solutions", None)])

def solution_page(u):
    s = SOL[u]; page = REF[u]; blks = blocks(page)
    hero_p = page["sections"][0]["p"]
    lead = next((x for x in hero_p if len(x) > 30), s["desc"])
    first = s.get("first") or "Discovery workshop"
    svc_links = next((sec_["links"] for sec_ in page["sections"] if sec_["eyebrow"].lower().startswith("related services")), [])
    svc_links = [(t, x) for t, x in svc_links if x.startswith("/services/")]
    same = [x for x in SOL if SOL[x]["group"] == s["group"] and x != u]
    same += [x for x in SOL if x != u and x not in same][:3 - len(same)] if len(same) < 3 else []
    nav = [(b["id"], b["label"]) for b in blks] + [("services", "Services"), ("more", "More solutions")]
    body = (P.hero(s["group"], s["title"], lead, s["img"], (s.get("tl") or "Scoped", "timeline, starting with: %s" % first), ("How it works", "#" + (blks[1]["id"] if len(blks) > 1 else "more")))
            + subnav(nav[:7], ("Book: %s" % first, "/contact"))
            + bands_from(blks)
            + stack("services", "Services behind this solution", "The practices that deliver it", "",
                    '<div class="svs">%s</div>' % "".join('<a class="sv" href="%s" data-r><span>%s</span><b>%s</b>%s</a>' % (x, E(PR[SVC[x][0]]["name"] if x in SVC else ("%s practice" % PR[PRACTICE_PATH[x]]["name"] if x in PRACTICE_PATH else "Service")), E(t), arrow()) for t, x in svc_links), "alt")
            + band("First step", first, "Every solution starts with a defined first step, so you can see the scope, the team and how results will be measured before committing to delivery.", ("Book: %s" % first, "/contact"))
            + stack("more", "More solutions", "Other solutions in %s" % s["group"], "", sol_cards(same[:3]))
            + contact("Discuss %s" % s["title"], "Share the process, systems and outcome you have in mind. We will confirm fit and scope the first step."))
    return shell(s["title"], page["desc"] or s["desc"], body, [("Home", "/"), ("Solutions", "/solutions"), (s["title"], None)])

# ---------------------------------------------------------------- industries
IND_LOGOS = {"banking": ["mastercard.svg", "group/santander.png", "broadridge.svg", "group/aviva.png", "zions-bancorporation.svg", "group/close-brothers.png", "group/bank-leumi.png"],
             "retail": ["group/asos.png", "nutrien.svg", "american-bureau-of-shipping.svg", "watts-water-technologies.png"],
             "energy": ["cmc-energy-services.png", "watts-water-technologies.png"],
             "government": ["insolvency-service.svg", "group/bristol-city-council.png", "group/royal-museums-greenwich.png", "group/public-health-england.png"],
             "higher-ed": ["queen-mary-university-of-london.svg"]}
IND_SERVICES = {
    "banking": [("Data & AI Governance", "/services/data-governance"), ("Custom AI Development", "/services/custom-ai"), ("Modernize Legacy Apps", "/services/legacy-modernisation"),
                ("Industry Clouds", "/services/sf-industries"), ("API Development & Management", "/services/api-dev"), ("Application Security", "/services/appsec")],
    "retail": [("Data Engineering", "/services/data-engineering"), ("Analytics", "/services/analytics"), ("Sales, Service & Marketing Cloud", "/services/sf-clouds"),
               ("S/4HANA Implementation & Migration", "/services/s4hana"), ("Integration Strategy", "/services/integration-strategy"), ("Business Process Automation", "/services/bpa")],
    "energy": [("Data Engineering", "/services/data-engineering"), ("Integration Strategy", "/services/integration-strategy"), ("API Development & Management", "/services/api-dev"),
               ("ERP Modernization", "/services/erp-modernization"), ("AI-Led Operations", "/services/ai-led-ops"), ("Cloud Migration & Integration", "/services/cloud-migration")],
    "government": [("Modernize Legacy Apps", "/services/legacy-modernisation"), ("Cloud Migration & Integration", "/services/cloud-migration"), ("Business Process Automation", "/services/bpa"),
                   ("Accessibility & Compliance", "/services/accessibility"), ("Data & AI Governance", "/services/data-governance"), ("ITSM, ITOM & AIOps", "/services/sn-itsm")],
    "legal": [("Managed Testing Services", "/services/managed-testing"), ("Performance Engineering", "/services/performance-engineering"), ("Analytics", "/services/analytics"),
              ("Generative AI", "/services/generative-ai"), ("Data & AI Governance", "/services/data-governance"), ("Business Process Automation", "/services/bpa")],
    "higher-ed": [("Analytics", "/services/analytics"), ("Data Engineering", "/services/data-engineering"), ("Sales, Service & Marketing Cloud", "/services/sf-clouds"),
                  ("HR Service Delivery & Employee", "/services/sn-employee"), ("Generative AI", "/services/generative-ai"), ("Accessibility & Compliance", "/services/accessibility")],
    "emerging": [("S/4HANA Implementation & Migration", "/services/s4hana"), ("ERP Modernization", "/services/erp-modernization"), ("SAP BTP & Integration", "/services/sap-btp"),
                 ("Cloud Migration & Integration", "/services/cloud-migration"), ("Data Engineering", "/services/data-engineering"), ("Maturity Assessments", "/services/maturity-assessments")],
}
HELP_ICONS = ["shield", "insight", "people", "layers", "data", "integration"]

def industry_page(path):
    key = path.rsplit("/", 1)[-1]; key = "emerging" if key == "emerging-markets" else key
    t, d, u, ic, im = next(x for x in INDUSTRIES if x[2] == path)
    page = REF[path]; secs = page["sections"]
    helps = next((s for s in secs if s["h"].lower().startswith("how prolifics helps")), None)
    chall = next((s for s in secs if "challenge" in s["h"].lower()), None)
    sols = [x for tt, x in next((s["links"] for s in secs if s["eyebrow"].lower().startswith("related solutions")), []) if x in SOL]
    cases = INDUSTRY_CASES.get(key, [])
    proof = next((LIB[c] for c in cases if LIB[c]["m"] and LIB[c]["m"] not in P.WEAK), None)
    card = (proof["m"], "%s, %s" % (proof["ml"], proof["client"])) if proof else ("150+", "Fortune 1000 clients across regulated and asset-intensive industries")
    nav, rest = [], ""
    lg = IND_LOGOS.get(key, [])
    strip = ('<section class="lstrip" aria-label="Selected clients"><div class="wrap ls-in"><p>Selected %s clients%s</p><ul>%s</ul>%s</div></section>' % (E(t.lower()), "<sup>*</sup>" if any(f.startswith("group/") for f in lg) else "", "".join("<li>%s</li>" % logo(f) for f in lg),
               '<p class="ls-n"><sup>*</sup>Includes clients of Prolifics group companies.</p>' if any(f.startswith("group/") for f in lg) else "")) if len(lg) >= 2 else ""
    if helps and helps["cards"]:
        hl = "".join('<li data-r><span class="eng-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (icon(HELP_ICONS[i % 6], 26), E(c["t"]), E(c["d"])) for i, c in enumerate(helps["cards"]))
        rest += sec("help", "How we help", "Where Prolifics makes the difference in %s" % t.lower(), '<ul class="eng four">%s</ul>' % hl, "Delivered through advisory, co-delivery, build-operate-transfer or fully managed models.")
        nav.append(("help", "How we help"))
    if chall and chall["cards"]:
        rest += sec("challenges", "Industry challenges", "The problems we are asked to solve", P.caps([(c["t"], c["d"], None) for c in chall["cards"]]), "", "alt")
        nav.append(("challenges", "Challenges"))
    if cases:
        rest += stack("work", "Selected work", "Published results in %s" % t.lower(), "Case studies from Prolifics and its group companies. Each links to the published source.", case_grid(cases))
        nav.append(("work", "Selected work"))
    rest += sec("services", "Services", "Services that matter most in %s" % t.lower(),
                '<div class="svs">%s</div>' % "".join('<a class="sv" href="%s" data-r><span>%s</span><b>%s</b>%s</a>' % (x, E(PR[SVC[x][0]]["name"]), E(n), arrow()) for n, x in IND_SERVICES[key] if x in SVC), "", "alt")
    nav.append(("services", "Services"))
    rest += '<section class="ps"><div class="wrap">%s</div></section>' % related([(a, b, c) for a, b, c, dd, ee in INDUSTRIES if c != path][:4], "More industries")
    rest += contact("Talk to our %s team" % t.lower(), "Bring the workflow, the systems it touches and the requirements around it. We will come back with a scoped first step.")
    body = (P.hero(t, page["h1"], lead_of(page), im, card, ("See selected work", "#work") if cases else ("Services", "#services"), wide=True)
            + strip + subnav(nav, ("Talk to Our Experts", "/contact")) + rest)
    return shell(t, page["desc"] or d, body, [("Home", "/"), ("Industries", "/industries"), (t, None)])

# ---------------------------------------------------------------- about, leadership, careers, social impact, ESG, locations
PHOTOS = {"Satya Bolli": "satya-bolli-2.png", "Greg Hodgkinson": "Greg-1.png", "Biju S. Nair": "Biju-Nair.webp", "Chetan Bolli": "chetan-1.png",
          "Ravi Thalluri": "ravi-1.png", "Kalyan Ganjam": "Kalyan-Ganjam.png", "Rakesh Kurchkulla": "Rakhesh-1.png"}

def leaders():
    from bs4 import BeautifulSoup
    s = BeautifulSoup(open(os.path.join(os.path.dirname(HERE), "ref", "about__leadership.html"), encoding="utf-8").read(), "html.parser")
    out = []
    for h in s.find("main").find_all("h3"):
        box = h.parent
        while len(box.find_all("h3")) == 1 and box.parent and len(box.parent.find_all("h3")) == 1: box = box.parent
        role = box.find("p"); role = re.sub(r"\s+", " ", role.get_text(" ", strip=True)) if role else ""
        full = re.sub(r"\s+", " ", box.get_text(" ", strip=True)); name = h.get_text(strip=True)
        bio = re.sub(r"^[A-Z]{2,3}\s+", "", full.replace(name, "", 1).replace(role, "", 1).strip()).replace("\u2019", "'")
        out.append((name, role, bio))
    return out

def person(name):
    f = PHOTOS.get(name)
    if f: return '<img src="assets/people/%s.webp" alt="%s" loading="lazy">' % (slug(name), E(name))
    return '<span class="mono" aria-hidden="true">%s</span>' % E("".join(w[0] for w in name.split()[:2]))

def about_page():
    page = REF["/about"]; secs = page["sections"]
    mv = secs[1]["cards"]
    tl = [re.match(r"(\d{4}) (.*)", x).groups() for x in secs[2]["li"]]
    tl_html = '<ol class="tline" data-r>%s</ol>' % "".join('<li><span class="tl-y">%s</span><p>%s</p></li>' % (E(y), E(t)) for y, t in tl)
    values = ["Thought Leadership & Innovation", "Accountability", "Customer-Centric", "Trust & Teamwork"]
    vals = '<ul class="vals">%s</ul>' % "".join('<li data-r><span class="cap-n">%02d</span><b>%s</b></li>' % (i + 1, E(v)) for i, v in enumerate(values))
    acc = '<ul class="acc2">%s</ul>' % "".join('<li data-r><span class="ac-y">%s</span><b>%s</b><span>%s</span></li>' % (E(y), E(c["t"]), E(c["d"])) for c, y in zip(secs[3]["cards"], ["2025", "2025", "2025", "2025", "2022", "2020", "2020", "2019", "2018"]))
    grp = '<ul class="grp2">%s</ul>' % "".join('<li data-r>%s<div><h3>%s</h3><p>%s</p></div></li>' % (H.group_logo(t), E(t), E(d)) for t, d, ic in GROUP)
    off = '<ul class="offs">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % (E(r), E(c)) for r, c in OFFICES)
    ld = leaders()[0]
    lead_card = ('<div class="ldr-f" data-r>%s<div><p class="eyebrow">Leadership</p><blockquote>%s</blockquote><p class="ldr-n"><b>%s</b>, %s</p><a class="lnk" href="/about/leadership">Meet the leadership team %s</a></div></div>'
                 % (person(ld[0]), E(REF["/about/leadership"]["sections"][0]["p"][0]), E(ld[0]), E(ld[1]), arrow()))
    body = (P.hero("About Prolifics", page["h1"], lead_of(page), "promo", ("1978", "founded in New York as JYACC"), ("Our story", "#story"))
            + subnav([("mission", "Mission"), ("story", "Our story"), ("values", "Values"), ("recognition", "Recognition"), ("group", "Group"), ("leadership", "Leadership")], ("Talk to Our Experts", "/contact"))
            + '<section class="ps" id="mission"><div class="wrap"><div class="mv">%s</div></div></section>' % "".join('<div class="mv-c" data-r><p class="eyebrow">%s</p><p class="mv-t">%s</p></div>' % (lab, E(c["t"])) for lab, c in zip(["Our mission", "Our vision"], mv))
            + P.facts()
            + stack("story", "Our story", secs[2]["h"], secs[2]["p"][0] if secs[2]["p"] else "", tl_html)
            + sec("values", "Our values", "What we hold ourselves to", vals, "", "alt")
            + stack("recognition", "Accomplishments", "Recognition for the work", "", acc)
            + sec("group", "One group", "Specialist firms, one account team", grp, "Specialist firms brought together under one name, so a client works with one team across platforms, testing and data.", "alt")
            + sec("offices", "Global reach", "13 offices in 6 countries", off + '<a class="lnk" href="/about/locations">All locations %s</a>' % arrow())
            + '<section class="ps alt" id="leadership"><div class="wrap">%s</div></section>' % lead_card
            + H.logo_grid(P.GRID_LOGOS, P.ASPECT, "Trusted by 150+ Fortune 1000 clients", "clients")
            + contact("Work with a team that has done this for 48 years", "Tell us the process, the platform and the result you need. We will come back with a scoped first step."))
    return shell("About Prolifics", page["desc"], body, [("Home", "/"), ("About Us", None)])

def leadership_page():
    page = REF["/about/leadership"]; L = leaders()
    cards = "".join('<li class="ldr" data-r><span class="ldr-im">%s</span><b>%s</b><span class="ldr-r">%s</span><p>%s</p></li>' % (person(n), E(n), E(r), E(b)) for n, r, b in L)
    q = page["sections"][0]["p"][0]
    body = ('<section class="ph slim lq"><div class="wrap ph-in"><div class="ph-t"><p class="kick">Leadership</p><h1>%s</h1><blockquote class="lq-q">%s</blockquote><p class="lq-n">Satya Bolli, Chairman and Managing Director</p></div>'
            '<figure class="lq-f">%s</figure></div></section>' % (E(page["h1"]), E(q.strip('"')), person("Satya Bolli"))
            + stack("team", "Meet our leadership team", "The people leading Prolifics", page["sections"][1]["p"][0] if page["sections"][1]["p"] else "", '<ul class="ldrs">%s</ul>' % cards)
            + contact("Talk to our leadership team", "Tell us what you want to achieve. A Prolifics expert in your industry and platform will get back to you."))
    return shell("Leadership", page["desc"], body, [("Home", "/"), ("About Us", "/about"), ("Leadership", None)])

def careers_page():
    page = REF["/about/careers"]; s = page["sections"]
    disc = P.caps([(c["t"], c["d"], None) for c in s[2]["cards"]])
    off = '<ul class="offs">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % (E(r), E(c)) for r, c in OFFICES)
    body = (P.hero("Careers", page["h1"], lead_of(page), "team2", ("2,000+", "experts across North America, Europe, the Middle East and India"), ("Find open roles", "#roles"))
            + subnav([("roles", "Open roles"), ("disciplines", "Disciplines"), ("offices", "Where we work")], ("View Open Roles", "https://prolifics.zohorecruit.in/jobs/Careers"))
            + band("Open roles", s[1]["h"], s[1]["p"][0], ("View Open Roles", "https://prolifics.zohorecruit.in/jobs/Careers")).replace('class="band"', 'class="band" id="roles"')
            + sec("disciplines", "Disciplines", s[2]["h"], disc)
            + sec("offices", "Where we work", "13 offices in 6 countries", off + '<a class="lnk" href="/about/locations">All locations %s</a>' % arrow(), "", "alt")
            + sec("why", "Why Prolifics", "Work on the platforms enterprises run", '<ul class="grp2">%s</ul>' % "".join('<li data-r>%s<div><h3>%s</h3><p>%s</p></div></li>' % (H.group_logo(t), E(t), E(d)) for t, d, ic in GROUP),
                  "Specialist firms brought together under one name: integration, Salesforce, SAP and testing in one group.")
            + contact("Learn about the team and our work", s[3]["p"][0] if len(s) > 3 and s[3]["p"] else "Explore our company, locations and practices."))
    return shell("Careers", page["desc"], body, [("Home", "/"), ("About Us", "/about"), ("Careers", None)])

def simple_about(path, image, crumb):
    page = REF[path]; s = page["sections"]
    rest, nav, i = "", [], 0
    for x in s[1:]:
        if not x["cards"] or x["eyebrow"].lower().startswith("more in"): continue
        id_ = slug(x["h"]); nav.append((id_, short(x["h"])))
        hl = "".join('<li data-r><span class="eng-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (icon(HELP_ICONS[j % 6], 26), E(c["t"]), E(c["d"])) for j, c in enumerate(x["cards"]))
        rest += sec(id_, crumb, x["h"], '<ul class="eng four">%s</ul>' % hl, "", "alt" if i % 2 else ""); i += 1
    more = [(t, d, u) for (t, d, u) in [(a, b, c) for g, l in ABOUT for a, b, c in l] if u.startswith("/about") and u != path][:4]
    body = (P.hero(crumb, page["h1"], lead_of(page), image, ("48 years", "of enterprise engineering, founded in New York in 1978"), ("Read more", "#" + (nav[0][0] if nav else "more")))
            + subnav(nav, ("Talk to Our Experts", "/contact")) + rest
            + '<section class="ps" id="more"><div class="wrap">%s</div></section>' % related(more, "More about Prolifics")
            + contact("Talk to us", "Tell us what you want to achieve. A Prolifics expert will get back to you."))
    return shell(crumb, page["desc"], body, [("Home", "/"), ("About Us", "/about"), (crumb, None)])

def locations_page():
    from bs4 import BeautifulSoup
    s = BeautifulSoup(open(os.path.join(os.path.dirname(HERE), "ref", "about__locations.html"), encoding="utf-8").read(), "html.parser")
    offs = []
    for a in s.find_all("address"):
        g = lambda c: re.sub(r"\s+", " ", a.find(class_=c).get_text(" ", strip=True)) if a.find(class_=c) else ""
        tel = a.find("a", href=re.compile("^tel:")); mp = a.find("a", href=re.compile("maps"))
        offs.append((a.get("data-cat", ""), g("card__t"), g("card__d"), (tel.get_text(strip=True), tel["href"]) if tel else None, mp["href"] if mp else ""))
    regions = []
    for o in offs:
        if o[0] not in regions: regions.append(o[0])
    chips = ['<button type="button" class="fc2 on" data-f="all" aria-pressed="true">All %d</button>' % len(offs)] + ['<button type="button" class="fc2" data-f="%s" aria-pressed="false">%s</button>' % (slug(r), E(r)) for r in regions]
    cards = "".join('<address class="loc" data-g="%s" data-r><span class="loc-r">%s</span><b>%s</b><span class="loc-a">%s</span><span class="loc-f">%s%s</span></address>'
                    % (slug(r), E(r), E(n), E(ad), ('<a href="%s">%s</a>' % (t[1], E(t[0]))) if t else "", ('<a class="lnk" href="%s" rel="noopener">Directions %s</a>' % (m, arrow())) if m else "") for r, n, ad, t, m in offs)
    page = REF["/about/locations"]
    body = (P.hero("Locations", page["h1"], lead_of(page), "globe", ("13", "offices in 6 countries"), ("See all offices", "#offices"))
            + '<section class="ps" id="offices"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Offices</p><h2>Find your nearest Prolifics office</h2></header>'
              '<div class="fcs2" role="group" aria-label="Filter by region">%s</div><div class="locs" id="loc-list">%s</div></div></section>' % ("".join(chips), cards)
            + contact("Talk to Our Experts", "A Prolifics expert in your industry and platform will get back to you within one business day."))
    return shell("Locations", page["desc"], body, [("Home", "/"), ("About Us", "/about"), ("Locations", None)])

# ---------------------------------------------------------------- partnerships, resources, guides, contact
PARTNER_LOGO = {"IBM": "ibm.svg", "Salesforce": "salesforce.svg", "ServiceNow": "servicenow.svg", "SAP": "sap.svg", "Microsoft": "microsoft.svg", "Boomi": "boomi.svg",
                "AWS": "aws.svg", "MuleSoft": "mulesoft.svg", "Databricks": "databricks.png", "Red Hat": "red-hat.svg", "Snowflake": "snowflake.png",
                "Google Cloud": "google-cloud.png", "EDB": "edb.png", "Tricentis": "tricentis.png"}
PARTNER_PAGE = {"IBM": "/services/app-services", "Salesforce": "/services/salesforce", "ServiceNow": "/services/servicenow", "SAP": "/services/sap", "Microsoft": "/services/cloud-migration",
                "Boomi": "/services/integration-strategy", "AWS": "/services/cloud-migration", "MuleSoft": "/services/sf-integration", "Databricks": "/services/data-engineering",
                "Red Hat": "/services/platform-engineering", "Snowflake": "/services/data-engineering", "Google Cloud": "/services/cloud-migration", "EDB": "/services/database-migration",
                "Tricentis": "/services/ai-test-automation"}

def partnerships_page():
    page = REF["/partnerships"]; s = page["sections"]
    cards = "".join('<li class="pt" id="partner-%s" data-r><span class="pt-l"><img src="assets/partners/%s" alt="%s" loading="lazy"></span><p>%s</p><a class="lnk" href="%s">Related services %s</a></li>'
                    % (slug(c["t"]), PARTNER_LOGO[c["t"]], E(c["t"]), E(c["d"]), PARTNER_PAGE[c["t"]], arrow()) for c in s[1]["cards"])
    why = [(c["t"], c["d"].replace("Platinum-level partnerships with the world's top innovators.", "Long-standing alliances with IBM, Salesforce, ServiceNow, SAP, Microsoft and AWS.")) for c in s[2]["cards"]]
    whyh = "".join('<li data-r><span class="eng-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (icon(HELP_ICONS[j], 26), E(t), E(d)) for j, (t, d) in enumerate(why))
    gain = P.caps([(c["t"], c["d"], None) for c in s[3]["cards"]])
    import standing as S
    body = (P.hero("Partnerships", page["h1"], lead_of(page), "r09", ("14", "technology partners across platforms, data, cloud and testing"), ("Partner ecosystem", "#ecosystem"))
            + subnav([("ecosystem", "Ecosystem"), ("credentials", "Credentials"), ("why", "Why Prolifics"), ("gain", "What partners gain")], ("Talk to Our Experts", "/contact"))
            + '<section class="ps" id="ecosystem"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Technology partner ecosystem</p><h2>%s</h2><p class="ps-p">%s</p></header><ul class="pts">%s</ul></div></section>'
              % (E(s[1]["h"]), E(s[1]["p"][0] if s[1]["p"] else ""), cards)
            + '<div id="credentials">%s</div>' % S.section(img, arrow, '<p class="lab"><span>IBM + SAP</span>Partner credentials</p>', "v1")
            + sec("why", "Why Prolifics", s[2]["h"], '<ul class="eng four">%s</ul>' % whyh, s[2]["p"][0] if s[2]["p"] else "", "alt")
            + sec("gain", "Partner value", s[3]["h"], gain)
            + contact("Partner with Prolifics", "Talk to us about joint delivery, co-innovation and go-to-market with Prolifics."))
    return shell("Partnerships", page["desc"], body, [("Home", "/"), ("Partnerships", None)])

IND_LABEL = {"banking": "Banking & Finance", "healthcare": "Healthcare & Life Sciences", "retail": "Retail, CPG & Logistics", "energy": "Energy & Utilities",
             "government": "Government & Public Sector", "legal": "Legal", "emerging": "Emerging Markets", "other": "Other industries"}

def resources_page():
    page = REF["/resources"]
    guides = "".join('<a class="gd2" href="%s" data-r><span class="gd2-im">%s</span><span class="gd2-k">Planning guide</span><b>%s</b><span>%s</span></a>' % (u, img(im, ""), E(t), E(d)) for t, d, u, im in GUIDES)
    order = [k for k in LIB]
    used = []
    for k in order:
        if LIB[k]["url"] not in [LIB[x]["url"] for x in used]: used.append(k)
    inds = [i for i in IND_LABEL if any(LIB[k]["ind"][0] == i for k in used)]
    chips = ['<button type="button" class="fc2 on" data-f="all" aria-pressed="true">All %d</button>' % len(used)] + ['<button type="button" class="fc2" data-f="%s" aria-pressed="false">%s</button>' % (i, E(IND_LABEL[i])) for i in inds]
    cards = case_grid(used, 99)
    for k in used:
        cards = cards.replace('<a class="cc sw" href="%s"' % LIB[k]["url"], '<a class="cc sw" data-g="%s" href="%s"' % (LIB[k]["ind"][0], LIB[k]["url"]), 1)
    body = (P.hero("Resource Center", page["h1"], lead_of(page), "r03", (str(len(used)), "published case studies, filterable by industry"), ("Case studies", "#cases"))
            + subnav([("guides", "Planning guides"), ("library", "Library"), ("cases", "Case studies")], ("Talk to Our Experts", "/contact"))
            + stack("guides", "Planning guides", "Questions to answer before you start", "", '<div class="gd2s">%s</div>' % guides)
            + stack("library", "Library", "Blogs, case studies and news from Prolifics", "Everything published in the Prolifics resource center, newest first. Filter by type or search by topic.", library())
            + '<section class="ps alt" id="cases"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Case studies</p><h2>Published results from Prolifics and its group companies</h2>'
              '<p class="ps-p">Each card links to the published case study. Filter by industry.</p></header><div class="fcs2" role="group" aria-label="Filter by industry">%s</div><div id="cs-list">%s</div>'
              '<p class="note"><a class="lnk" href="#library">Browse every case study in the library %s</a></p></div></section>' % ("".join(chips), cards, arrow())
            + contact("Discuss your priorities", "Connect these planning questions to your delivery priorities across AI, data, Salesforce, ServiceNow and SAP.")
            + rs_assets())
    return shell("Resource Center", page["desc"], body, [("Home", "/"), ("Resources", None)])

# The library and the article page are filled in the browser by resources.js from /api/resources, which reads the
# corporate site (prolifics.ai) live. A post published there shows here within minutes; nothing needs rebuilding.
# dist/vercel.json rewrites /resources/article/<slug> to the one article shell.
RS_CSS = open(os.path.join(HERE, "resources.css"), encoding="utf-8").read()
RS_JS = open(os.path.join(HERE, "resources.js"), encoding="utf-8").read()
def rs_assets(): return "<style>%s</style><script>%s</script>" % (RS_CSS, RS_JS)

def library():
    return ('<div class="rs-bar"><div class="rs-f" id="rs-filters" role="group" aria-label="Filter by type" hidden></div>'
            '<form class="rs-s" id="rs-search" role="search"><input type="search" id="rs-q" name="q" maxlength="80" placeholder="Search the library" aria-label="Search the library">'
            '<button type="submit">Search</button></form></div>'
            '<div class="rs-list" id="rs-list" aria-live="polite"><p class="rs-note">Loading</p></div>'
            '<div class="rs-foot"><p class="rs-count" id="rs-count"></p><button type="button" class="rs-more" id="rs-more" hidden>Load more</button></div>'
            '<noscript><p class="rs-note">Turn on JavaScript to browse the library, or <a href="/contact">contact us</a>.</p></noscript>')

def resource_article():
    body = ('<section class="rs-top"><div class="wrap"><p class="rs-note" id="rs-wait">Loading</p>'
            '<article class="rs-art" id="rs-article" hidden><p class="kick" id="rs-type"></p><h1 id="rs-title"></h1><p class="rs-date" id="rs-date"></p>'
            '<figure class="rs-fig" id="rs-fig" hidden></figure><div class="rs-body" id="rs-body"></div>'
            '<a class="lnk" href="/resources#library">All resources %s</a></article>'
            '<noscript><p class="rs-note">Turn on JavaScript to read this resource, or <a href="/contact">contact us</a>.</p></noscript></div></section>'
            '<section class="rs-rel" id="rs-rel" hidden><div class="wrap"><h2 id="rs-rel-h">More resources</h2><div class="rs-list" id="rs-rel-list"></div></div></section>'
            % arrow()
            + contact("Discuss your priorities", "Connect what you have read to your delivery priorities across AI, data, Salesforce, ServiceNow and SAP.")
            + rs_assets())
    return shell("Resource Center", "Blogs, case studies and news from Prolifics.", body, [("Home", "/"), ("Resources", "/resources"), ("Article", None)])

def guide_page(path):
    page = REF[path]; s = page["sections"]
    parts = [x for x in s[1:] if x["h"] and not x["h"].lower().startswith(("explore related",))]
    toc = "".join('<li><a href="#%s">%s</a></li>' % (slug(x["h"]), E(re.sub(r"^\d+\.\s*", "", x["h"]))) for x in parts)
    rel = next((x["links"] for x in s if x["h"].lower().startswith("explore related")), [])
    rel_cards = [(t, "A Prolifics service", u) for t, u in rel if u.startswith("/services")][:3]
    content = "".join('<section class="dblk art" id="%s"><h2>%s</h2>%s</section>' % (slug(x["h"]), E(x["h"]), "".join("<p>%s</p>" % E(p) for p in x["p"])) for x in parts)
    content += related([(t, SVC[u][2] and PR[SVC[u][0]]["name"], u) if u in SVC else (t, "", u) for t, d, u in rel_cards], "Related services")
    other = [(t, d, u) for t, d, u, im in GUIDES if u != path]
    content += related(other, "More planning guides")
    im = next(im for t, d, u, im in GUIDES if u == path)
    body = ('<section class="ph slim"><div class="wrap ph-in"><div class="ph-t"><p class="kick">Planning guide</p><h1>%s</h1><p class="ph-lead">%s</p></div><figure class="gfig">%s</figure></div></section>'
            % (E(page["h1"]), E(lead_of(page)), img(im, "", "", True))
            + '<div class="detail"><div class="wrap det-in"><aside class="side"><nav class="toc" aria-label="In this guide"><p class="side-h">In this guide</p><ul>%s</ul></nav>'
              '<a class="side-cta" href="/contact"><b>Plan with an expert</b><span>Talk to Our Experts %s</span></a></aside><div class="det-c">%s</div></div></div>' % (toc, arrow(), content)
            + contact("Discuss your priorities", "Connect these planning questions to your delivery priorities across AI, data, Salesforce, ServiceNow and SAP."))
    return shell(page["h1"], page["desc"], body, [("Home", "/"), ("Resources", "/resources"), (page["h1"], None)])

def contact_page():
    page = REF["/contact"]
    phones = [("North America", "+1 (800) 458-3313", "tel:+18004583313"), ("United Kingdom", "+44 (0) 207 100 8666", "tel:+4402071008666"), ("UAE", "+971 5444 36585", "tel:+971544436585")]
    form = '<div class="cf">%s</div>' % P.hs_form("general")
    ph = "".join('<div><dt>%s</dt><dd><a href="%s">%s</a></dd></div>' % (E(r), u, E(n)) for r, n, u in phones) + '<div><dt>India</dt><dd><a href="/about/locations">Hyderabad and Pune offices</a></dd></div>'
    body = ('<section class="ct"><div class="wrap ct-in"><div class="ct-l"><p class="kick">Contact</p><h1>%s</h1><p class="ph-lead">%s</p><dl class="ct-ph">%s</dl>'
            '<a class="lnk" href="/about/locations">See all locations %s</a></div>%s</div></section>' % (E(page["h1"]), E(lead_of(page)), ph, arrow(), form)
            + H.logo_grid(P.GRID_LOGOS, P.ASPECT, "Trusted by 150+ Fortune 1000 clients", "clients"))
    return shell("Contact", page["desc"] or "Talk to Prolifics experts", body, [("Home", "/"), ("Contact", None)])

def thanks_page():
    body = ('<section class="ct"><div class="wrap"><div class="ct-l"><p class="kick">Contact</p><h1>Thank you</h1>'
            '<p class="ph-lead">We have your request. A Prolifics expert in your industry and platform will get back to you within one business day.</p>'
            '%s</div></div></section>' % ctas(("Back to the home page", "/"), ("Explore services", "/services")))
    return shell("Thank you", "Thank you for contacting Prolifics.", body, [("Home", "/"), ("Contact", "/contact"), ("Thank you", None)])

# ---------------------------------------------------------------- happenings (content comes from HubSpot)
# Both pages are empty shells: happenings.js fills them in the browser from /api/happenings, which reads the HubDB
# table "Happenings". Marketing adds, edits, reorders and hides entries in HubSpot; nothing here needs rebuilding.
# dist/vercel.json rewrites /happenings/<slug> to the one detail shell, so a new row gets its own page at once.
HP_CSS = open(os.path.join(HERE, "happenings.css"), encoding="utf-8").read()
HP_JS = open(os.path.join(HERE, "happenings.js"), encoding="utf-8").read()
def hp_assets(): return "<style>%s</style><script>%s</script>" % (HP_CSS, HP_JS)

def happenings_page():
    body = ('<section class="hp-top"><div class="wrap"><p class="kick">Events</p><h1>Events and campaigns at Prolifics</h1>'
            '<p class="ph-lead">Where to meet Prolifics next: events, webinars and campaigns from our teams and group companies.</p></div></section>'
            '<section class="hp-sec"><div class="wrap"><div class="hp-f" id="hp-filters" hidden></div>'
            '<div class="hp-list" id="hp-list" aria-live="polite"><p class="hp-note">Loading events</p></div>'
            '<noscript><p class="hp-note">Turn on JavaScript to see current events, or <a href="/contact">contact us</a>.</p></noscript></div></section>'
            + hp_assets())
    return shell("Events", "Events, webinars and campaigns from Prolifics and its group companies.", body, [("Home", "/"), ("Resources", "/resources"), ("Events", None)])

def happening_detail():
    form = P.hs_form("general").replace('<form class="lf"', '<form class="lf" data-ok="You are registered. We will email you the details." ', 1).replace(
        '<div class="cf-g">', '<input type="hidden" name="happening" value=""><div class="cf-g">', 1)
    body = ('<section class="hp-top hp-one" id="hp-one"><div class="wrap"><p class="hp-note" id="hp-wait">Loading</p>'
            '<div class="hp-dg" id="hp-detail" hidden><article class="hp-art"><p class="kick" id="hp-type"></p><h1 id="hp-name"></h1>'
            '<dl class="hp-meta" id="hp-meta"></dl><figure class="hp-fig" id="hp-fig" hidden></figure><p class="ph-lead" id="hp-sum"></p>'
            '<div class="hp-body" id="hp-body"></div><a class="lnk" href="/events">All events %s</a></article>'
            '<aside class="hp-reg" id="hp-reg" hidden><h2 id="hp-reg-h">Register</h2><div class="cf">%s</div></aside></div>'
            '<noscript><p class="hp-note">Turn on JavaScript to see this event, or <a href="/contact">contact us</a>.</p></noscript></div></section>'
            % (arrow(), form) + hp_assets())
    return shell("Events", "Events, webinars and campaigns from Prolifics.", body, [("Home", "/"), ("Resources", "/resources"), ("Events", "/events"), ("Details", None)])

# ---------------------------------------------------------------- group companies
def src_link(u): return ' <a class="src" href="%s" rel="noopener">source</a>' % E(u) if u else ""

def group_card(slug_, g, wide=False):
    return ('<a class="gcard" href="/group/%s" data-r><span class="gcard-l"><img src="assets/group/%s" alt="%s" loading="lazy"></span><span class="gcard-k">%s</span>'
            '<b>%s</b><span class="gcard-d">%s</span><span class="lnk">Explore %s %s</span></a>' % (slug_, g["logo"], E(g["name"]), E(g["kick"]), E(g["h1"]), E(g["lead"]), E(g["name"]), arrow()))

def group_landing():
    cards = "".join(group_card(k, g) for k, g in GROUP_PAGES.items())
    tl = [("2015", "Stream Integration", "Information management and analytics, folded into the Prolifics data practice"),
          ("2017", "e-testing", "UK testing consultancy, today Prolifics Testing"), ("2022", "Tier 2 Consulting", "UK custom software and Red Hat expertise"),
          ("2023", "Enable Consulting", "The Salesforce practice"), ("2025", "Castaliaz", "SAP S/4HANA and managed SAP support in India")]
    tlh = '<ol class="tline">%s</ol>' % "".join('<li><span class="tl-y">%s</span><p><b>%s</b><br>%s</p></li>' % (y, E(n), E(d)) for y, n, d in tl)
    how = P.caps([("One account team", "A client works with one Prolifics team across Salesforce, SAP, testing, data and custom software, not five vendors.", None),
                  ("Specialists stay specialists", "Each firm keeps its depth and its people, and works inside the matching Prolifics practice.", None),
                  ("Testing in every program", "Prolifics Testing brings quality engineering and agent evaluation into work across the group.", None),
                  ("Global delivery", "North America, the UK and Europe, the Middle East and India, with 13 offices in 6 countries.", None)])
    body = (P.hero("Group companies", "One group, one account team", "Specialist firms brought together under the Prolifics name, so clients get Salesforce, SAP, quality engineering and custom software depth from one team.",
                   "k_summit", ("4", "specialist firms working inside the Prolifics practices"), ("Meet the firms", "#firms"))
            + subnav([("firms", "The firms"), ("how", "How it works"), ("history", "How the group formed"), ("clients", "Clients")], ("Talk to Our Experts", "/contact"))
            + '<section class="ps" id="firms"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">The firms</p><h2>Four specialist firms, each inside a Prolifics practice</h2></header><div class="gcards">%s</div></div></section>' % cards
            + sec("how", "How it works", "What a group means for a client", how, "", "alt")
            + stack("history", "How the group formed", "A decade of adding depth where clients needed it", "Acquisition dates from the companies' announcements.", tlh)
            + H.logo_grid(None, P.ASPECT, "Clients across the Prolifics group", "clients")
            + contact("Talk to the Prolifics group", "Tell us the platform and the outcome. We will bring the right firm and the right practice to the first conversation."))
    return shell("Group companies", "The Prolifics group: Enable Consulting, Castaliaz, Prolifics Testing and Tier 2 Consulting.", body, [("Home", "/"), ("About Us", "/about"), ("Group companies", None)])

def group_page(k):
    g = GROUP_PAGES[k]
    facts = "".join('<div><dt>%s</dt><dd>%s%s</dd></div>' % (E(a), E(b), src_link(u)) for a, b, u in g["facts"])
    facts += '<div><dt>Prolifics practice</dt><dd><a href="%s">%s</a></dd></div>' % (g["practice"][1], E(g["practice"][0]))
    if g["site"]: facts += '<div><dt>Website</dt><dd><a href="%s" rel="noopener">%s</a></dd></div>' % (g["site"], E(g["site"].split("//")[1].strip("/")))
    hero = ('<section class="ph slim"><div class="wrap ph-in"><div class="ph-t"><span class="g-hl"><img src="assets/group/%s" alt="%s"></span><p class="kick">%s</p><h1>%s</h1><p class="ph-lead">%s</p>%s</div>'
            '<aside class="kf" aria-label="At a glance"><p class="side-h">At a glance</p><dl>%s</dl></aside></div></section>'
            % (g["logo"], E(g["name"]), E(g["kick"]), E(g["h1"]), E(g["lead"]), ctas(("Talk to Our Experts", "#talk"), ("What %s offers" % g["name"], "#offers")), facts))
    nav = [("offers", "Offerings"), ("where", "Sectors")]
    rest = sec("offers", "Offerings", "What %s does" % g["name"], P.caps([(t, d, None) for t, d in g["offers"]]) + '<p class="note">As described on %s.%s</p>' % (E(g["name"] + "'s own site" if g["site"] else "the AppExchange listing"), src_link(g["offers_src"])))
    chips = '<div class="pchips">%s</div>' % "".join('<span class="pchip">%s</span>' % E(x) for x in g["sectors"])
    cred = ('<p class="sub-h">Accreditations and partners</p><ul class="chk">%s</ul>' % "".join('<li>%s<span>%s%s</span></li>' % (icon("check", 20), E(t), src_link(u)) for t, u in g["creds"])) if g["creds"] else ""
    rest += sec("where", "Sectors", "Where %s works" % g["name"], chips + cred, "", "alt")
    if g.get("work"):
        rows = "".join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (E(a), E(b), E(c)) for a, b, c in g["work"])
        rest += sec("work", "Published work", "Results %s has published" % g["name"],
                    '<div class="tbl" data-r><table><thead><tr><th>Client</th><th>Engagement</th><th>Result</th></tr></thead><tbody>%s</tbody></table></div><p class="note">From %s case studies.%s</p>' % (rows, E(g["name"]), src_link(g["work_src"])))
        nav.append(("work", "Published work"))
    if g["cases"]:
        rest += stack("cases", "Case studies", "Related work across the group", "Each card links to the published case study.", case_grid(g["cases"], 4 if len(g["cases"]) == 4 else 3), "alt")
        nav.append(("cases", "Case studies"))
    if len(g["logos"]) >= 2:
        rest += ('<section class="lstrip" aria-label="Selected clients"><div class="wrap ls-in"><p>Selected %s clients</p><ul>%s</ul></div></section>' % (E(g["name"]), "".join("<li>%s</li>" % logo(f) for f in g["logos"])))
    rest += band("In the Prolifics group", "Part of the %s practice" % g["practice"][0],
                 "%s works inside the Prolifics %s practice, so clients get the firm's specialists with Prolifics integration, data, testing and global delivery around them." % (g["name"], g["practice"][0]),
                 ("Explore %s" % g["practice"][0], g["practice"][1]))
    others = [(v["name"], v["kick"], "/group/" + kk) for kk, v in GROUP_PAGES.items() if kk != k] + [("All group companies", "One group, one account team", "/group")]
    rest += '<section class="ps"><div class="wrap">%s</div></section>' % related(others, "More of the Prolifics group")
    rest += contact("Talk to %s and Prolifics" % g["name"], "Share the platform, the process and the outcome. We will bring the right specialists to the first conversation.")
    return shell(g["name"], "%s, a Prolifics group company: %s" % (g["name"], g["lead"]), hero + subnav(nav, ("Talk to Our Experts", "#talk")) + rest,
                 [("Home", "/"), ("About Us", "/about"), ("Group companies", "/group"), (g["name"], None)])

# ---------------------------------------------------------------- page list and write
def all_pages():
    pages = dict(P.PAGES)
    for k in ["ai", "fde", "sn", "sap", "app", "bt", "qe"]:
        pages[PR[k]["href"].lstrip("/")] = (lambda k=k: practice_page(k))
    for u in REF:
        if u.startswith("/services/") and u not in PRACTICE_PATH and u.lstrip("/") not in pages:
            pages[u.lstrip("/")] = (lambda u=u: service_page(u))
    for t, d, u, ic, im in INDUSTRIES:
        if u != "/industries/healthcare": pages[u.lstrip("/")] = (lambda u=u: industry_page(u))
    pages.update({"about": about_page, "about/leadership": leadership_page, "about/careers": careers_page, "about/locations": locations_page,
                  "about/social-impact": lambda: simple_about("/about/social-impact", "r02", "Social Impact"),
                  "about/esg": lambda: simple_about("/about/esg", "i_powerlines_1", "ESG Vision"),
                  "partnerships": partnerships_page, "resources": resources_page, "contact": contact_page, "thank-you": thanks_page,
                  "events": happenings_page, "events/detail": happening_detail, "resources/article": resource_article})
    for t, d, u, im in GUIDES: pages[u.lstrip("/")] = (lambda u=u: guide_page(u))
    pages["group"] = group_landing
    for k in GROUP_PAGES: pages["group/" + k] = (lambda k=k: group_page(k))
    return pages

def assets():
    for f in set(LOGOS) | {c[0] for c in CASES} | set(HC["logos"]) | {x for v in IND_LOGOS.values() for x in v} | {x for k, t, fs in WALL for x in fs}:
        P.ASPECT[f] = prep(os.path.join(H.GTM, "clients", f), os.path.join(DIST, "assets", "clients", f))
    os.makedirs(os.path.join(DIST, "assets", "people"), exist_ok=True)
    for n, f in PHOTOS.items():
        im = Image.open(os.path.join(HERE, "people", f)).convert("RGBA"); im.thumbnail((640, 640))
        im.save(os.path.join(DIST, "assets", "people", slug(n) + ".webp"), "WEBP", quality=80)
    for f in PARTNER_LOGO.values():
        prep(os.path.join(HERE, "partners", f), os.path.join(DIST, "assets", "partners", f))

if __name__ == "__main__":
    P.FINAL = "--final" in sys.argv
    if not os.path.exists(os.path.join(DIST, "index.html")): sys.exit("Run build_home.py first")
    assets()
    pages = all_pages()
    total_d = total_x = 0
    for path, fn in sorted(pages.items()):
        u = "/" + path
        P.FORM["key"] = (PRACTICE_PATH.get(u) or (SVC[u][0] if u in SVC else None) or ("sf" if u == "/services/agentforce" else None)
                         or (GROUP_PAGES[path[6:]]["form"] if path.startswith("group/") else None)
                         or ("solutions" if path.startswith("solutions") else "general"))
        out, n, b = optimize(fn(), os.path.join(HERE, "img2"), os.path.join(DIST, "assets", "img"))
        out = P.absolutize(out)
        d = os.path.join(DIST, path); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S); vis = re.sub(r"<[^>]+>", " ", text)
        dashes = len(re.findall("[–—]", text)) + text.count("&mdash;") + text.count("&ndash;"); ex = vis.count("!")
        total_d += dashes; total_x += ex
        if dashes or ex: print("  %s: dashes %d, exclamation %d" % (path, dashes, ex))
    vc = {"headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}], "trailingSlash": False,
          # Solutions removed from the site (Mac, 23 Nov 2026): old links land on Services
          "redirects": [{"source": "/happenings", "destination": "/events", "permanent": False},   # renamed to Events, 28 Nov 2026
                        {"source": "/happenings/:slug", "destination": "/events/:slug", "permanent": False},
                        {"source": "/solutions", "destination": "/services", "permanent": False},
                        {"source": "/solutions/:p*", "destination": "/services", "permanent": False}],
          # every happening, and every library article, shares one page shell; the script on it reads the slug from the address
          "rewrites": [{"source": "/events/:slug", "destination": "/events/detail"},
                       {"source": "/resources/article/:slug", "destination": "/resources/article"}]}
    json.dump(vc, open(os.path.join(DIST, "vercel.json"), "w"), indent=1)
    shutil.copytree(os.path.join(HERE, "api"), os.path.join(DIST, "api"), dirs_exist_ok=True)   # /api/lead: sends form submissions to HubSpot
    print("%d pages, dashes %d, exclamation %d" % (len(pages) + 1, total_d, total_x))
