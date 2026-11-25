# -*- coding: utf-8 -*-
"""Inner pages for approval (22 Nov 2026): Services landing, Salesforce practice, Agentforce service detail,
Industries landing and Healthcare industry detail. Writes into ../dist next to the home page, so run
build_home.py first:  python3 src/build_home.py && python3 src/build_pages.py   (add --final to drop noindex)
Design direction: consulting style (KPMG, Bain, BCG): white ground, strong type hierarchy, left-hand section
titles, breadcrumbs and in-page navigation on every page, brand navy for feature bands."""
import os, re, json, sys
import build_home as H
from content import *
from pages_content import *
from icons import icon
from optimize import optimize
from logoutil import prep, size

E, arrow, img = H.E, H.arrow, H.img
HERE, DIST = H.HERE, H.DIST
FINAL = "--final" in sys.argv
CASE = {c[0]: c for c in CASES}
PR = {p["k"]: p for p in PRACTICES}
ASPECT = {}
WEAK = {"1"}   # metrics too small to lead a card; the card shows the story instead

# ---------------------------------------------------------------- building blocks
def crumbs(items):
    li = "".join(('<li><a href="%s">%s</a></li>' % (u, E(t))) if u else ('<li aria-current="page">%s</li>' % E(t)) for t, u in items)
    return '<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>%s</ol></div></nav>' % li

def ctas(primary=("Talk to Our Experts", "/contact"), second=None):
    s = '<a class="btn btn-p" href="%s">%s</a>' % (primary[1], E(primary[0]))
    if second: s += '<a class="btn btn-o" href="%s">%s %s</a>' % (second[1], E(second[0]), arrow())
    return '<div class="ctas">%s</div>' % s

def hero(kick, h1, lead, image, card=None, second=None, wide=False):
    c = ('<figcaption class="ph-card"><b>%s</b><span>%s</span></figcaption>' % (E(card[0]), E(card[1]))) if card else ""
    cls = "ph wide" if wide else "ph"
    return ('<section class="%s"><div class="wrap ph-in"><div class="ph-t"><p class="kick">%s</p><h1>%s</h1><p class="ph-lead">%s</p>%s</div>'
            '<figure class="ph-fig">%s%s</figure></div></section>' % (cls, E(kick), E(h1), E(lead), ctas(second=second), img(image, "", "", True), c))

def subnav(items, cta=None):
    li = "".join('<li><a href="#%s">%s</a></li>' % (a, E(t)) for a, t in items)
    c = '<a class="sn-cta" href="%s">%s %s</a>' % (cta[1], E(cta[0]), arrow()) if cta else ""
    return '<nav class="subnav" aria-label="On this page"><div class="wrap sn-in"><ul>%s</ul>%s</div></nav>' % (li, c)

def sec(id_, eyebrow, title, body, intro="", cls=""):
    i = '<p class="ps-p">%s</p>' % E(intro) if intro else ""
    if "stack" in cls:
        return ('<section class="ps %s" id="%s"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">%s</p><h2>%s</h2>%s</header>'
                '%s</div></section>' % (cls, id_, E(eyebrow), E(title), i, body))
    return ('<section class="ps %s" id="%s"><div class="wrap ps-in"><header class="ps-h" data-r><p class="eyebrow">%s</p><h2>%s</h2>%s</header>'
            '<div class="ps-b">%s</div></div></section>' % (cls, id_, E(eyebrow), E(title), i, body))

def facts():
    return ('<section class="facts" aria-label="Prolifics at a glance"><div class="wrap fx">%s</div></section>'
            % "".join('<div class="fx-c" data-r><p class="fx-n" data-count="%s">%s</p><p class="fx-l">%s</p><p class="fx-d">%s</p></div>'
                      % (n, n, E(l), E(d)) for n, l, d, s, u in STATS))

def caps(items, numbered=True):
    return '<ol class="caps">%s</ol>' % "".join(
        '<li data-r><span class="cap-n">%02d</span><h3>%s</h3><p>%s</p>%s</li>'
        % (i + 1, E(t), E(d), ('<a class="lnk" href="%s">Explore %s</a>' % (u, arrow())) if u else "")
        for i, (t, d, u) in enumerate(items))

def steps(items):
    return '<ol class="steps" data-r>%s</ol>' % "".join(
        '<li><span class="st-dot">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, E(t), E(d)) for i, (t, d) in enumerate(items))

def table(rows, head=("Measure", "What to assess")):
    return ('<div class="tbl" data-r><table><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>'
            % (E(head[0]), E(head[1]), "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (E(a), E(b)) for a, b in rows)))

def faq(items):
    return '<div class="faq">%s</div>' % "".join(
        '<details%s><summary>%s<span class="fq-x" aria-hidden="true"></span></summary><p>%s</p></details>' % (" open" if i == 0 else "", E(q), E(a))
        for i, (q, a) in enumerate(items))

def example(text, label="Illustrative delivery scenario"):
    return ('<aside class="ex" data-r><p class="ex-k">%s</p><p>%s</p><p class="ex-n">A design example, not a claim about a completed client deployment.</p></aside>'
            % (E(label), E(text)))

def logo(f, cls=""):
    h, w = size(ASPECT.get(f, 3.0))
    alt = CASE[f][1] if f in CASE else re.sub(r"[-_]", " ", f.rsplit("/", 1)[-1].rsplit(".", 1)[0]).title()
    return '<img class="%s" src="assets/clients/%s" alt="%s" width="%d" height="%d" loading="lazy">' % (cls, f, E(alt), w, h)

def case_cards(files):
    out = []
    for f in files:
        _, client, sector, by, title, brief, m, ml, im, u = CASE[f]
        out.append('<a class="cc" href="%s" rel="noopener" data-r><span class="cc-im">%s<span class="chip-i">%s</span></span><span class="cc-b">%s%s'
                   '<span class="cc-t">%s</span><span class="cc-d">%s</span><span class="cc-f"><span>Delivered by %s</span></span>'
                   '<span class="cc-x">Read the case study %s</span></span></a>'
                   % (u, img(im, ""), E(sector), logo(f, "cc-lg"), "" if m in WEAK else '<span class="cc-m"><b>%s</b><span>%s</span></span>' % (E(m), E(ml)), E(title), E(brief), E(by), arrow()))
    return '<div class="ccs">%s</div>' % "".join(out)

def related(items, title="Explore related expertise"):
    return ('<div class="rel"><p class="rel-h">%s</p><div class="rel-g">%s</div></div>' % (E(title), "".join(
        '<a class="rl" href="%s" data-r><b>%s</b><span>%s</span><span class="rl-x">%s</span></a>' % (u, E(t), E(d), arrow()) for t, d, u in items)))

def band(eyebrow, title, text, cta):
    return ('<section class="band"><div class="wrap band-in" data-r><div><p class="eyebrow">%s</p><h2>%s</h2></div><div><p>%s</p>'
            '<a class="btn btn-c" href="%s">%s %s</a></div></div></section>' % (E(eyebrow), E(title), E(text), cta[1], E(cta[0]), arrow()))

# HubSpot forms in the Prolifics portal (8077126), created 22 Nov 2026 by cloning "Prolifics new contact form"
# (restyled for white pages). One per practice plus Solutions and General Contact. HubSpot records the page URL of
# every submission, so reports can still split by individual service page.
PORTAL = "8077126"
FORMS = {"ai": "44477275-4b25-44a6-8d63-35ab5b1805ad", "fde": "09cebf58-d31b-4789-8594-8d75016fdc52",
         "sf": "770410e5-bbd4-4488-bcf0-7b0e2cb8d6bb", "sn": "d9261c64-8c64-47cd-b4f9-df15365f0157",
         "sap": "1b72d9b5-c1b7-470a-83d0-83dca7968c11", "app": "23ff4485-d0aa-46f6-98fb-45e17784110b",
         "bt": "e4b0d1cd-bb32-43cb-8b78-d0dd0f6ef5fc", "qe": "10fb9988-1b78-47f8-af87-f864e2ee42f2",
         "solutions": "d3e700db-c885-421e-99f8-caf567f4b21e", "general": "a63a4cb4-4803-4425-b135-ddbf740dfa43"}
FORM = {"key": "general"}   # set per page by the site builder

# Native lead form (25 Nov 2026), replacing the HubSpot embed. HubSpot collects it through the tracking script on
# every page (H.TRACK, "non-HubSpot forms"), which only works while the form stays plain HTML: an <input type="email">,
# an <input type="submit"> and NO JavaScript on the form's submit or the button's click. Do not add a submit handler.
# The form posts to /api/lead (src/api/lead.js, copied into dist/api by build_site.py), which only redirects to
# /thank-you. Only first name, last name and work email are required (browser validation).
INTEREST = [("ai", "AI and Data"), ("fde", "FDE AI Engineering"), ("sf", "Salesforce"), ("sn", "ServiceNow"), ("sap", "SAP and ERP"),
            ("app", "Application and Cloud"), ("bt", "Business Transformation"), ("qe", "Quality Engineering"), ("general", "Not sure yet")]
COUNTRIES = ["United States", "Canada", "United Kingdom", "Ireland", "Germany", "France", "Netherlands", "Spain", "Italy", "Switzerland",
             "Sweden", "United Arab Emirates", "Saudi Arabia", "Qatar", "India", "Singapore", "Australia", "Japan", "Brazil", "Mexico",
             "South Africa", "Other"]

def hs_form(key=None):
    key = key or FORM["key"]
    assert key in FORMS
    def lab(t, req): return '<span>%s%s</span>' % (E(t), '<i aria-hidden="true">*</i>' if req else '<em>Optional</em>')
    def inp(name, t, typ="text", req=False, ac="off", ph=""):
        return ('<label class="fld">%s<input type="%s" name="%s" autocomplete="%s"%s%s></label>'
                % (lab(t, req), typ, name, ac, ' placeholder="%s"' % E(ph) if ph else "", " required" if req else ""))
    def sel(name, t, opts, cur=None):
        return ('<label class="fld">%s<select name="%s"><option value="">Select</option>%s</select></label>'
                % (lab(t, False), name, "".join('<option value="%s"%s>%s</option>' % (E(l), " selected" if v == cur else "", E(l)) for v, l in opts)))
    return ('<form class="lf" data-form="%s" method="post" action="/api/lead"><div class="cf-g">%s%s%s%s%s%s%s%s</div>'
            '<label class="fld wide">%s<textarea name="message" rows="4" placeholder="The outcome you want, the systems involved and your timing"></textarea></label>'
            '<label class="lf-ck"><input type="checkbox" name="marketing_opt_in"><span>Send me Prolifics insights and event invitations. I can unsubscribe at any time.</span></label>'
            '<input class="btn btn-p" type="submit" value="Talk to Our Experts">'
            '<div class="cf-p">By submitting, you agree that Prolifics may use these details to respond to your request, as described in the '
            '<a href="https://prolifics.ai/privacy-policy" rel="noopener">Privacy Policy</a>.</div></form>'
            % (key, inp("firstname", "First name", req=True, ac="given-name"), inp("lastname", "Last name", req=True, ac="family-name"),
               inp("email", "Work email", "email", True, "email", "name@company.com"), inp("phone", "Phone", "tel", ac="tel"),
               inp("company", "Company", ac="organization"), inp("jobtitle", "Job title", ac="organization-title"),
               sel("country", "Country", [(c, c) for c in COUNTRIES]), sel("interest", "Area of interest", INTEREST, key),
               lab("How can we help?", False)))

def contact(title, text):
    return ('<section class="talk" id="talk"><div class="wrap talk-in"><div data-r><p class="eyebrow">Next step</p><h2>%s</h2><p>%s</p>'
            '<p class="talk-n">Prefer to talk? See phone numbers for every region on the <a href="/contact">contact page</a> or find your nearest office on the '
            '<a href="/about/locations">locations page</a>.</p></div><div class="talk-f">%s</div></div></section>' % (E(title), E(text), hs_form()))

def engage():
    return '<ul class="eng">%s</ul>' % "".join(
        '<li data-r><span class="eng-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (icon(ic, 26), E(t), E(d)) for t, d, ic in ENGAGE)

def sprint():
    return '<ol class="spr4" data-r>%s</ol>' % "".join(
        '<li><p class="s4-w">%s</p><p class="s4-t">%s</p><p class="s4-d">%s</p></li>' % (E(w), E(t), E(d)) for w, t, d in SPRINT)

# ---------------------------------------------------------------- page shell
PCSS = open(os.path.join(HERE, "pages.css"), encoding="utf-8").read()
PJS = open(os.path.join(HERE, "pages.js"), encoding="utf-8").read()

def shell(title, desc, body, crumb):
    robots = "" if FINAL else '<meta name="robots" content="noindex, nofollow">'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">%s'
            '<title>%s | Prolifics</title><meta name="description" content="%s">'
            '<script>document.documentElement.className+=" js"</script><meta name="theme-color" content="#FFFFFF"><link rel="icon" href="assets/favicon.png">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
            '<style>%s%s</style></head><body class="inner">'
            '<a class="skip" href="#main">Skip to content</a>%s%s%s<main id="main">%s</main>%s<script>%s%s</script>%s</body></html>'
            % (robots, E(title), E(desc), H.CSS, PCSS, H.header(), H.drawer(), crumbs(crumb), body, H.footer(), H.JS, PJS, H.TRACK))

# ---------------------------------------------------------------- 1. Services landing
def services():
    jump = "".join('<a class="jl" href="#%s"><span>%02d</span>%s</a>' % (k, i + 1, E(t)) for i, (k, t, d, ks) in enumerate(SVC_CATS))
    cats = []
    n = 0
    for k, t, d, ks in SVC_CATS:
        rows = []
        for key in ks:
            p = PR[key]; n += 1
            nsv = sum(len(l) for h, l in p["groups"])
            groups = "".join('<div class="pg2"><h4>%s</h4><ul>%s</ul></div>' % (E(h), "".join('<li><a href="%s">%s</a></li>' % (u, E(x)) for x, u in links)) for h, links in p["groups"])
            rows.append('<article class="prc" id="%s" data-r><a class="prc-im" href="%s" tabindex="-1" aria-hidden="true">%s</a><div class="prc-b">'
                        '<p class="prc-k">%s<span>%d services</span></p><h3><a href="%s">%s</a></h3><p class="prc-d">%s</p><div class="pg2s">%s</div>'
                        '<div class="prc-f"><a class="btn btn-p sm" href="%s">Explore %s %s</a><a class="lnk" href="%s">Start with: %s %s</a></div></div></article>'
                        % (p["k"], p["href"], img(p["img"], ""), icon(p["icon"], 22), nsv, p["href"], E(p["name"]), E(p["long"]), groups,
                           p["href"], E(p["name"]), arrow(), p["start"][1], E(p["start"][0]), arrow()))
        cats.append('<div class="cat" id="%s"><header class="cat-h" data-r><h2>%s</h2><p>%s</p></header>%s</div>' % (k, E(t), E(d), "".join(rows)))
    idx = "".join('<a class="ix" href="#%s">%s<b>%s</b><span>%s</span></a>' % (p["k"], icon(p["icon"], 24), E(p["name"]), E(p["desc"])) for p in PRACTICES)
    pr = "".join('<li data-r><h3>%s</h3><p>%s</p></li>' % (E(t), E(d)) for t, d in PRINCIPLES)
    grp = "".join('<li data-r>%s<div><h3>%s</h3><p>%s</p></div></li>' % (H.group_logo(t), E(t), E(d)) for t, d, ic in GROUP)
    guides = "".join('<a class="gd2" href="%s" data-r><span class="gd2-im">%s</span><span class="gd2-k">Planning guide</span><b>%s</b><span>%s</span></a>'
                     % (u, img(im, ""), E(t), E(d)) for t, d, u, im in GUIDES)
    body = (hero(SVC_HERO["kick"], SVC_HERO["h1"], SVC_HERO["lead"], "k_light", SVC_HERO["card"], ("How we engage", "#engage"))
            + subnav([("practices", "Practices"), ("principles", "How we work"), ("engage", "Ways to engage"), ("results", "Results"), ("group", "Specialist firms"), ("insights", "Insights")],
                     ("Talk to Our Experts", "/contact"))
            + '<section class="ps idx-s" id="practices"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Our practices</p>'
              '<h2>Eight practices, grouped by the outcome you need</h2><div class="jls">%s</div></header><div class="ixg" data-r>%s</div></div></section>' % (jump, idx)
            + '<div class="cats"><div class="wrap">%s</div></div>' % "".join(cats)
            + facts()
            + sec("principles", "How we work", "One delivery standard across every practice", '<ul class="prin">%s</ul>' % pr,
                  "Whatever the platform, the way we start, measure and hand over stays the same.")
            + sec("engage", "Ways to engage", "Four models, chosen by who should own the result", engage() + '<p class="sub-h">How a forward deployed sprint runs</p>' + sprint(),
                  "Start with advice, build alongside your engineers, or hand us the whole service.", "alt")
            + sec("results", "Results", "Measured outcomes from published case studies", case_cards(["horizon-bcbs-nj.png", "rac.svg", "mckesson.svg"]),
                  "Work by Prolifics and its group companies, each linked to the published case study.", "stack")
            + sec("group", "Specialist firms", "One group, one account team", '<ul class="grp2">%s</ul>' % grp,
                  "Specialist firms brought together under one name, so a client works with one team across platforms, testing and data.", "alt")
            + sec("insights", "Insights", "Questions to answer before you start", '<div class="gd2s">%s</div>' % guides)
            + contact("Bring one process. Leave with it in production.",
                      "Tell us the process, the platform and the result you need. We will come back with a scoped first step, the team and how we will measure it."))
    return shell("Services", "Prolifics services: AI and data, forward deployed engineering, Salesforce, ServiceNow, SAP, application and cloud, business transformation and quality engineering.",
                 body, [("Home", "/"), ("Services", None)])

# ---------------------------------------------------------------- 2. Salesforce practice (v2, after Mac's review)
GRID_LOGOS = [f for f in LOGOS if f != "cmc-energy-services.png"][:18]

def sf_hero():
    c1, c2 = SF2["cards"]
    return ('<section class="ph sfh"><div class="wrap ph-in"><div class="ph-t"><p class="kick">%s</p><h1>%s</h1><p class="ph-lead">%s</p>%s'
            '<ul class="sfh-tags"><li>9 services</li><li>6 industries</li><li>Agentforce, Data 360, MuleSoft</li></ul></div>'
            '<figure class="ph-fig sfh-fig">%s<figcaption class="fl fl1"><b>%s</b><span>%s</span></figcaption>'
            '<figcaption class="fl fl2"><b>%s</b><span>%s</span></figcaption></figure></div></section>'
            % (E(SF2["kick"]), E(SF2["h1"]), E(SF2["lead"]), ctas(second=("Explore Salesforce services", "#services")),
               img(SF2["img"], "", "", True), E(c1[0]), E(c1[1]), E(c2[0]), E(c2[1])))

def why_now():
    cells = "".join('<div class="wn-c" data-r><p class="wn-n">%s</p><p class="wn-t">%s</p><a class="wn-s" href="%s" rel="noopener">%s</a></div>'
                    % (st["n"], E(st["t"]), E(st["u"]), E(st["s"])) for st in SFD["stats"])
    return ('<section class="wn" id="why"><div class="wrap"><div class="wn-h" data-r><p class="eyebrow">Why now</p><h2>Agentforce is scaling fast. '
            'Integration decides who reaches production.</h2></div><div class="wn-g">%s</div></div></section>' % cells)

def agents_change():
    cards = "".join('<li data-r><span class="ac-n">%02d</span><span class="eng-ic">%s</span><h3>%s</h3><p>%s</p></li>'
                    % (i + 1, icon(x["icon"], 26), E(x["t"]), E(x["d"])) for i, x in enumerate(SFD["ai_first"]))
    return ('<section class="ps alt" id="change"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">AI first</p>'
            '<h2>What agents change about Salesforce work</h2><p class="ps-p">The CRM is no longer only a system people type into. It is where agents read '
            'context, take actions and leave an audit trail.</p></header><ul class="acg">%s</ul></div></section>' % cards)

def explorer():
    tabs, panels = [], []
    for i, o in enumerate(SFD["offers"]):
        sel = i == 0
        tabs.append('<button type="button" class="cx-t" role="tab" id="cxt-%s" aria-controls="cxp-%s" aria-selected="%s" tabindex="%d">'
                    '<span class="cx-n">%02d</span><span class="cx-l"><b>%s</b><small>%s</small></span></button>'
                    % (o["slug"], o["slug"], "true" if sel else "false", 0 if sel else -1, i + 1, E(o["name"]), E(o["nav"])))
        scope = "".join("<li>%s%s</li>" % (icon("check", 18), E(x)) for x in o["scope"])
        en = o["entry"]
        panels.append('<div class="cx-p" role="tabpanel" id="cxp-%s" aria-labelledby="cxt-%s"%s><div class="cx-ph"><span class="cx-ic">%s</span><div><p class="cx-k">Service %02d of 9</p>'
                      '<h3>%s</h3></div></div><p class="cx-s">%s</p><p class="cx-h">What is in scope</p><ul class="cx-sc">%s</ul>'
                      '<div class="cx-e"><p class="cx-ek">Start with</p><p class="cx-en"><b>%s</b><span>%s</span></p><p class="cx-ed">%s</p></div>'
                      '<a class="lnk" href="/contact">Talk to us about %s %s</a></div>'
                      % (o["slug"], o["slug"], "" if sel else " hidden", icon(o["icon"], 30), i + 1, E(o["name"]), E(o["summary"]), scope,
                         E(en["name"]), E(en["length"]), E(en["d"]), E(o["name"]), arrow()))
    menu = "".join('<a href="%s">%s</a>' % (u, E(t)) for h, links in PR["sf"]["groups"] for t, u in links)
    return ('<section class="ps" id="services"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Capabilities</p>'
            '<h2>Nine Salesforce services, led by certified people and forward deployed pods</h2><p class="ps-p">Most clients start by adding certified '
            'engineers to their team, then put one Agentforce workflow into production with a pod. Every service opens with a fixed-scope entry of 2 to 6 weeks.</p></header>'
            '<div class="cx" data-r><div class="cx-tl" role="tablist" aria-label="Salesforce services">%s</div><div class="cx-ps">%s</div></div>'
            '<div class="sfm"><p>Every Salesforce service page</p><div>%s</div></div></div></section>' % ("".join(tabs), "".join(panels), menu))

def sf_industries():
    tiles = []
    for x in SFD["industries"]:
        key = x["slug"].split("-")[0]
        pr = SF_PROOF.get(key)
        proof = ('<span class="si-p"><small>Proof</small>%s: %s</span>' % (E(SF_WORK[pr][0]), E(SF_WORK[pr][2]))) if pr is not None else \
                '<span class="si-p"><small>Service</small>Financial Services Cloud and agents</span>'
        tiles.append('<li class="si" data-r>%s<span class="si-sh"></span><span class="si-b"><span class="si-ic">%s</span><b>%s</b><span class="si-d">%s</span>%s</span></li>'
                     % (img(x["img"], ""), icon(x["icon"], 22), E(x["name"]), E(x["summary"]), proof))
    return ('<section class="ps" id="industries"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Industries we serve</p>'
            '<h2>Six industries where integration and control decide whether agents reach production</h2><p class="ps-p">Where Prolifics and Enable '
            'Consulting bring delivery history, with the published work behind it.</p></header><ul class="sig">%s</ul></div></section>' % "".join(tiles))

def sf_work():
    cards = []
    for client, ind, title, brief, m, ml, im, lg, by, u in SF_WORK:
        head = logo(lg, "cc-lg") if lg else '<span class="cc-cl">%s</span>' % E(client)
        met = '<span class="cc-m"><b>%s</b><span>%s</span></span>' % (E(m), E(ml)) if m else ""
        cards.append('<a class="cc sw" href="%s" rel="noopener" data-r><span class="cc-im">%s<span class="chip-i">%s</span></span><span class="cc-b">%s%s'
                     '<span class="cc-t">%s</span><span class="cc-d">%s</span><span class="cc-f"><span>Delivered by %s</span></span>'
                     '<span class="cc-x">Read the case study %s</span></span></a>' % (u, img(im, ""), E(ind), head, met, E(title), E(brief), E(by), arrow()))
    q, who, qu = SF_QUOTE
    quote = ('<figure class="qt" data-r><span class="qt-m" aria-hidden="true">&ldquo;</span><blockquote>%s</blockquote><figcaption>%s, '
             '<a href="%s" rel="noopener">from the published case study</a></figcaption></figure>' % (E(q), E(who), qu))
    return ('<section class="ps alt" id="work"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">Selected Salesforce work</p>'
            '<h2>Six published stories, across six industries</h2><p class="ps-p">Delivered by Prolifics and Enable Consulting, a Salesforce partner since 2002 '
            'and part of Prolifics since September 2023.</p></header><div class="ccs">%s</div>%s</div></section>' % ("".join(cards), quote))

def salesforce():
    body = (sf_hero()
            + subnav([("clients", "Clients"), ("why", "Why now"), ("services", "Services"), ("industries", "Industries"), ("work", "Work"),
                      ("approach", "Approach"), ("faq", "FAQ")], ("Agentforce Readiness Assessment", "/services/agentforce"))
            + H.logo_grid(GRID_LOGOS, ASPECT, "Selected clients across the Prolifics group", "clients")
            + why_now() + agents_change() + explorer() + sf_industries() + sf_work()
            + sec("approach", "Approach", "Start with the customer journey, then engineer the platform", steps(SF["steps"]))
            + band("Agentforce readiness", "What a readiness review should establish", SF["readiness"], ("Agentforce Readiness Assessment", "/services/agentforce"))
            + sec("engage", "Ways to engage", "Advisory, co-delivery, build-operate-transfer or fully managed", engage()
                  + '<a class="pod" href="/services/fde-ai-engineering" data-r>%s<span><b>Salesforce and Agentforce Pod</b><span>A forward deployed pod embeds with your business owner and ships one workflow at a time.</span></span>%s</a>' % (icon("pod", 28), arrow()))
            + sec("faq", "FAQ", "Salesforce: frequently asked questions", faq(SF["faq"]), "", "alt")
            + '<section class="ps"><div class="wrap">%s</div></section>' % related(SF["related"])
            + contact("Bring us one Salesforce workflow to discuss",
                      "Share the process, systems and outcome you have in mind. We will discuss the dependencies, scope and the right next step with your team."))
    return shell("Salesforce Consulting and Agentforce Implementation",
                 "Salesforce consulting and Agentforce implementation from Prolifics and Enable Consulting: certified engineers, forward deployed pods, Data 360 and MuleSoft integration, industry clouds and managed services.",
                 body, [("Home", "/"), ("Services", "/services"), ("Salesforce", None)])

# ---------------------------------------------------------------- 3. Agentforce service detail (sidebar layout)
def agentforce():
    p = PR["sf"]
    toc = [("who", "Who this is for"), ("work", "What we deliver"), ("path", "From use case to release"), ("prepare", "What to bring"),
           ("measure", "How we measure"), ("faq", "FAQ")]
    sib = "".join('<li><p>%s</p><ul>%s</ul></li>' % (E(h), "".join('<li><a href="%s"%s>%s</a></li>' % (u, ' aria-current="page"' if u == "/services/agentforce" else "", E(t)) for t, u in links))
                  for h, links in p["groups"])
    aside = ('<aside class="side"><nav class="toc" aria-label="On this page"><p class="side-h">On this page</p><ul>%s</ul></nav>'
             '<nav class="sibs" aria-label="Salesforce services"><p class="side-h">Salesforce services</p><ul>%s</ul></nav>'
             '<a class="side-cta" href="/contact"><b>Plan your first agent</b><span>Talk to a Salesforce expert %s</span></a></aside>'
             % ("".join('<li><a href="#%s">%s</a></li>' % (a, E(t)) for a, t in toc), sib, arrow()))
    work = "".join('<li data-r><span class="cap-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, E(t), E(d)) for i, (t, d) in enumerate(AF["work"]))
    bring = "".join('<li>%s%s</li>' % (icon("check", 20), E(b)) for b in AF["bring"])
    blk = lambda id_, eyebrow, title, inner: '<section class="dblk" id="%s"><p class="eyebrow">%s</p><h2>%s</h2>%s</section>' % (id_, E(eyebrow), E(title), inner)
    content = (blk("who", "Who this is for", "Hands-on agent delivery, ready for production", '<p class="big-p">%s</p>' % E(AF["who"]))
               + blk("work", "What we deliver", "Implementation work from the use case to operations", '<ol class="caps two">%s</ol>' % work)
               + blk("path", "Approach", "Move from a candidate use case to an accepted release", steps(AF["steps"]))
               + blk("prepare", "Before we start", "Prepare the workflow, users and approved data",
                     '<ul class="chk">%s</ul><p class="note">Implementation scope depends on these dependencies. Learning workshops can support the receiving team, but training does not replace release testing or operational handover.</p>' % bring
                     + example(AF["example"], "Example: a bounded service case action"))
               + blk("measure", "Measurement", "Agree the baseline before measuring the result", table(AF["measures"])
                     + '<p class="note">Select measures for the agreed scope and compare like for like work before and after release. Targets are set with your process owners.</p>')
               + blk("faq", "FAQ", "Agentforce implementation: frequently asked questions", faq(AF["faq"]))
               + related(AF["related"], "Related services and guides"))
    kf = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(a), b) for a, b in [
        ("Practice", '<a href="/services/salesforce">Salesforce</a>'), ("Delivered with", "Enable Consulting, a Salesforce partner since 2002"),
        ("Ways to engage", "Advisory, co-delivery, build-operate-transfer, fully managed"),
        ("Forward deployed option", '<a href="/services/fde-ai-engineering">Salesforce and Agentforce Pod</a>')])
    hero_ = ('<section class="ph slim"><div class="wrap ph-in"><div class="ph-t"><p class="kick">%s</p><h1>%s</h1><p class="ph-lead">%s</p>%s</div>'
             '<aside class="kf" aria-label="At a glance"><p class="side-h">At a glance</p><dl>%s</dl></aside></div></section>'
             % (E(AF["kick"]), E(AF["h1"]), E(AF["lead"]), ctas(("Discuss your Agentforce priorities", "/contact"), ("Explore the delivery approach", "#path")), kf))
    body = (hero_ + '<div class="detail"><div class="wrap det-in">%s<div class="det-c">%s</div></div></div>' % (aside, content)
            + contact("Bring us one workflow to discuss", "Share the process, systems and outcome you have in mind. We will discuss the dependencies, scope and the right next step with your team."))
    return shell("Agentforce Implementation Services", "Agentforce implementation from Prolifics: workflow and architecture, grounding and data access, actions and integration, evaluation and release.",
                 body, [("Home", "/"), ("Services", "/services"), ("Salesforce", "/services/salesforce"), ("Agentforce Implementation", None)])

# ---------------------------------------------------------------- 4. Industries landing
def industries():
    tiles = "".join('<a class="itl" href="%s" data-r><span class="itl-im">%s</span><span class="itl-b"><span class="itl-ic">%s</span><b>%s</b><span>%s</span>'
                    '<span class="lnk">Explore %s</span></span></a>' % (u, img(im, ""), icon(ic, 22), E(t), E(d), arrow()) for t, d, u, ic, im in INDUSTRIES)
    trs = "".join('<tr><td><span class="rt-c">%s<b>%s</b></span></td><td>%s</td><td>%s</td><td>%s</td><td><a class="lnk" href="%s" rel="noopener">Read %s</a></td></tr>'
                  % (logo(f, "rt-lg"), E(client), E(sector), E(title) if m in WEAK else '<b class="rt-m">%s</b> %s' % (E(m), E(ml)), E(by), u, arrow())
                  for f, client, sector, by, title, brief, m, ml, im, u in CASES)
    work = ('<div class="tbl rt" data-r><table><thead><tr><th>Client</th><th>Sector</th><th>Result</th><th>Delivered by</th><th><span class="vh">Case study</span></th></tr></thead>'
            '<tbody>%s</tbody></table></div>' % trs)
    chips = "".join('<a class="pchip" href="%s">%s%s</a>' % (p["href"], icon(p["icon"], 18), E(p["name"])) for p in PRACTICES)
    body = (hero(IND_HERO["kick"], IND_HERO["h1"], IND_HERO["lead"], "i_aerial_port_2", ("150+", "Fortune 1000 clients across regulated and asset-intensive industries"))
            + subnav([("all", "All industries"), ("work", "Selected work"), ("capabilities", "Capabilities")], ("Talk to Our Experts", "/contact"))
            + '<section class="ps" id="all"><div class="wrap"><header class="ps-h wide" data-r><p class="eyebrow">All industries</p><h2>Eight industries, one engineering standard</h2>'
              '<p class="ps-p">Select an industry to see its priorities, the services that matter most and the work we have published.</p></header><div class="itls">%s</div></div></section>' % tiles
            + sec("work", "Selected work", "Published results across industries", work,
                  "Case studies from Prolifics and its group companies. Each links to the published source.", "alt stack")
            + sec("capabilities", "Capabilities", "Every industry draws on the same eight practices", '<div class="pchips" data-r>%s</div>' % chips,
                  "Industry context shapes the workflow. The engineering underneath stays consistent.")
            + contact("Start with a business process", "Bring the workflow, systems and outcome you have in mind. We will discuss the right combination of industry context, platform expertise and engineering delivery."))
    return shell("Industries", "Prolifics industry expertise: banking, healthcare and life sciences, retail and logistics, energy and utilities, government, legal, higher education and emerging markets.",
                 body, [("Home", "/"), ("Industries", None)])

# ---------------------------------------------------------------- 5. Healthcare industry detail
def healthcare():
    help_ = "".join('<li data-r><span class="eng-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (icon(ic, 26), E(t), E(d)) for t, d, ic in HC["help"])
    ch = "".join('<li data-r><span class="cap-n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, E(t), E(d)) for i, (t, d) in enumerate(HC["challenges"]))
    lg = "".join('<li>%s</li>' % logo(f) for f in HC["logos"])
    svc = "".join('<a class="sv" href="%s" data-r><span>%s</span><b>%s</b>%s</a>' % (u, E(pr), E(t), arrow()) for t, u, pr in HC["services"])
    st, sd, su, stl = HC["solution"]
    sol = ('<a class="solc" href="%s" data-r><span class="solc-k">Packaged solution</span><b>%s</b><span>%s</span><span class="solc-f"><span>%s</span>'
           '<span class="lnk">Explore the solution %s</span></span></a>' % (su, E(st), E(sd), E(stl), arrow()))
    body = (hero(HC["kick"], HC["h1"], HC["lead"], "i_hosp_arch_4", ("60M", "claims a year through automated handling at Horizon Blue Cross Blue Shield of New Jersey"),
                 ("See selected work", "#work"), wide=True)
            + '<section class="lstrip" aria-label="Selected healthcare and life sciences clients"><div class="wrap ls-in"><p>Selected healthcare and life sciences clients<sup>*</sup></p><ul>%s</ul><p class="ls-n"><sup>*</sup>Includes clients of Prolifics group companies.</p></div></section>' % lg
            + subnav([("help", "How we help"), ("challenges", "Challenges"), ("work", "Selected work"), ("services", "Services")], ("Talk to Our Experts", "/contact"))
            + sec("help", "How we help", "Interoperable, compliant and ready for AI", '<ul class="eng four">%s</ul>' % help_,
                  "Delivered through advisory, co-delivery, build-operate-transfer or fully managed models.")
            + sec("challenges", "Industry challenges", "The problems we are asked to solve", '<ol class="caps">%s</ol>' % ch, "", "alt")
            + sec("work", "Selected work", "Results in health insurance, distribution and credentialing", case_cards(HC["cases"]),
                  "Published case studies from Prolifics, Prolifics Testing and Enable Consulting.", "stack")
            + sec("services", "Services", "Services that matter most in healthcare", '<div class="svs">%s</div>' % svc, "", "alt")
            + '<section class="ps"><div class="wrap">%s</div></section>' % related([(t, d, u) for t, d, u, ic, im in INDUSTRIES if u != "/industries/healthcare"][:4], "More industries")
            + contact("Talk to our healthcare and life sciences team", "Bring the workflow, the systems it touches and the compliance requirements around it. We will come back with a scoped first step."))
    return shell("Healthcare and Life Sciences", "Prolifics for healthcare and life sciences: interoperability, patient and member engagement, compliance-ready data and governed AI.",
                 body, [("Home", "/"), ("Industries", "/industries"), ("Healthcare & Life Sciences", None)])

# ---------------------------------------------------------------- write
PAGES = {"services": services, "services/salesforce": salesforce, "services/agentforce": agentforce,
         "industries": industries, "industries/healthcare": healthcare}

def absolutize(h):
    return re.sub(r'(["(])assets/', r'\1/assets/', h)

if __name__ == "__main__":
    if not os.path.exists(os.path.join(DIST, "index.html")):
        sys.exit("Run build_home.py first")
    for f in set(c[0] for c in CASES) | set(HC["logos"]) | set(LOGOS):
        ASPECT[f] = prep(os.path.join(H.GTM, "clients", f), os.path.join(DIST, "assets", "clients", f))
    total_d = total_x = 0
    for path, fn in PAGES.items():
        out, n, b = optimize(fn(), os.path.join(HERE, "img2"), os.path.join(DIST, "assets", "img"))
        out = absolutize(out)
        d = os.path.join(DIST, path); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S)
        vis = re.sub(r"<[^>]+>", " ", text)
        dashes = len(re.findall("[–—]", text)) + text.count("&mdash;") + text.count("&ndash;")
        total_d += dashes; total_x += vis.count("!")
        print("%-24s %7d bytes, %2d images, dashes %d, exclamation %d" % (path, len(out), n, dashes, vis.count("!")))
    # vercel.json: built pages are served from dist, everything else still goes to the reference site
    built = [p for p in PAGES]
    vc = json.load(open(os.path.join(DIST, "vercel.json")))
    vc["redirects"] = [
        {"source": "/services/:p((?!salesforce$|agentforce$).+)", "destination": "https://prolifics-website.vercel.app/services/:p", "permanent": False},
        {"source": "/solutions/:p*", "destination": "https://prolifics-website.vercel.app/solutions/:p*", "permanent": False},
        {"source": "/solutions", "destination": "https://prolifics-website.vercel.app/solutions", "permanent": False},
        {"source": "/industries/:p((?!healthcare$).+)", "destination": "https://prolifics-website.vercel.app/industries/:p", "permanent": False},
    ] + [r for r in vc["redirects"] if not r["source"].startswith(("/services", "/solutions", "/industries"))]
    vc["trailingSlash"] = False
    json.dump(vc, open(os.path.join(DIST, "vercel.json"), "w"), indent=1)
    print("total dashes %d, exclamation %d" % (total_d, total_x))
