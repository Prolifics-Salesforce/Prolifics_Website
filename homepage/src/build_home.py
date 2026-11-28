# -*- coding: utf-8 -*-
"""Builds the Prolifics home page into ../dist. Run: python3 src/build_home.py  (add --noindex to keep search engines out)
v2 art direction: full color photography and abstract imagery, editorial layout, animated 48 year hero."""
import os, re, shutil, json, html, sys
from content import *
from icons import icon
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DIST = os.path.join(PROJ, "dist")
GTM = os.path.join(HERE, "brand")   # Prolifics logos, favicon and client logos (copied from the GTM project, Nov 2026)
E = lambda s: html.escape(s, quote=True)

def img(name, alt="", cls="", eager=False, sizes=""):
    return '<img class="%s" src="assets/img/%s.jpg" alt="%s" %s decoding="async">' % (cls, name, E(alt), 'fetchpriority="high"' if eager else 'loading="lazy"')

def arrow():
    return '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4.5L12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

def label(n, t, light=False):
    return '<p class="lab%s"><span>%s</span>%s</p>' % (" lab-l" if light else "", n, E(t))

# ---------------------------------------------------------------- Google Tag Manager (28 Nov 2026)
# The standard container snippet, on every page: the script high in <head>, the noscript frame first in <body>.
# Google Analytics 4 runs as a tag inside the container, so there is no separate gtag snippet. Change the container
# by setting GTM_ID in the environment when building, or by editing the default here.
GTM_ID = os.environ.get("GTM_ID", "GTM-P5ZMJ49Q")
GTM_HEAD = ("<!-- Google Tag Manager --><script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
            "})(window,document,'script','dataLayer','" + GTM_ID + "');</script><!-- End Google Tag Manager -->")
GTM_BODY = ('<!-- Google Tag Manager (noscript) --><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' + GTM_ID + '" '
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript><!-- End Google Tag Manager (noscript) -->')

# ---------------------------------------------------------------- header and mega menus (menu from the reference site)
def mega_services():
    rail, panes = [], []
    items = PRACTICES + [{"k": "tech", "name": "Technologies", "desc": "The platforms our engineers build on every day.", "icon": "integration"}]
    for i, p in enumerate(items):
        if p["k"] == "tech":
            rail.append('<li class="mega-lab">Platforms</li>')
        rail.append('<li><button type="button" class="rail-b%s" data-pane="m-%s" aria-controls="m-%s">%s<span>%s</span></button></li>'
                    % (" on" if i == 0 else "", p["k"], p["k"], icon(p["icon"], 20), E(p["name"])))
        if p["k"] == "tech":
            body = "".join('<div class="mg"><h4>%s</h4><div class="chips">%s</div></div>' % (E(h), "".join('<span class="chip">%s</span>' % E(c) for c in cs)) for h, cs in TECH)
            head = '<div class="mp-h"><div><p class="mp-t">Technologies</p><p class="mp-d">%s</p></div><a class="lnk" href="/partnerships">Partnerships %s</a></div>' % (E(p["desc"]), arrow())
        else:
            body = "".join('<div class="mg"><h4>%s</h4><ul>%s</ul></div>' % (E(h), "".join('<li><a href="%s">%s</a></li>' % (u, E(t)) for t, u in links)) for h, links in p["groups"])
            head = '<div class="mp-h"><div><p class="mp-t">%s</p><p class="mp-d">%s</p></div><a class="lnk" href="%s">View overview %s</a></div>' % (E(p["name"]), E(p["desc"]), p["href"], arrow())
        panes.append('<div class="mp" id="m-%s" role="region" aria-label="%s"%s>%s<div class="mgs">%s</div></div>'
                     % (p["k"], E(p["name"]), "" if i == 0 else " hidden", head, body))
    return ('<div class="mega" id="mega-services" hidden><div class="wrap mega-in svc"><ul class="rail"><li class="mega-lab">Services</li>%s</ul>'
            '<div class="panes">%s</div></div></div>' % ("".join(rail), "".join(panes)))

def mega_solutions():
    cols = "".join('<div class="mg"><h4>%s</h4><ul class="rich">%s</ul></div>' % (E(g), "".join(
        '<li><a href="%s"><b>%s</b><span>%s</span></a></li>' % (u, E(t), E(d)) for t, d, u, ic, tl in items)) for g, items in SOLUTIONS)
    return ('<div class="mega" id="mega-solutions" hidden><div class="wrap mega-in"><div class="mp-h"><div><p class="mp-t">Solutions</p>'
            '<p class="mp-d">Packaged offers with a defined scope, clear timeline and a simple first step.</p></div>'
            '<a class="lnk" href="/solutions">All solutions %s</a></div><div class="mgs g3">%s</div></div></div>' % (arrow(), cols))

def mega_industries():
    cells = "".join('<a class="ind-l" href="%s">%s<span><b>%s</b><small>%s</small></span></a>' % (u, img(im, ""), E(t), E(d)) for t, d, u, ic, im in INDUSTRIES)
    return ('<div class="mega" id="mega-industries" hidden><div class="wrap mega-in"><div class="mp-h"><div><p class="mp-t">Industries</p>'
            '<p class="mp-d">150+ Fortune 1000 clients across regulated and asset-intensive industries.</p></div><a class="lnk" href="/industries">Explore all industries %s</a></div>'
            '<div class="ind-g">%s</div></div></div>' % (arrow(), cells))

def mega_about():
    cols = "".join('<div class="mg"><h4>%s</h4><ul class="rich">%s</ul></div>' % (E(h), "".join(
        '<li><a href="%s"><b>%s</b><span>%s</span></a></li>' % (u, E(t), E(d)) for t, d, u in links)) for h, links in ABOUT)
    promo = ('<a class="promo" href="/about">%s<span class="promo-t"><small>Celebrating 48 years</small><b>Engineering firsts since 1978.</b>'
             '<em>48 years, 2,000+ experts, 13 offices in 6 countries</em></span></a>' % img("promo", ""))
    return '<div class="mega" id="mega-about" hidden><div class="wrap mega-in abt"><div class="mgs g2">%s</div>%s</div></div>' % (cols, promo)

def mega_resources():
    cols = "".join('<div class="mg"><h4>%s</h4><ul class="rich">%s</ul></div>' % (E(h), "".join(
        '<li><a href="%s"%s><b>%s</b><span>%s</span></a></li>' % (u, ' rel="noopener"' if u.startswith("http") else "", E(t), E(d)) for t, d, u in links)) for h, links in RESOURCES_MENU)
    return '<div class="mega" id="mega-resources" hidden><div class="wrap mega-in"><div class="mgs g2">%s</div></div></div>' % cols

def header():
    nav = [("Services", "services"), ("Industries", "industries"), ("Partnerships", "/partnerships"),
           ("Resources", "resources"), ("About Us", "about")]
    lis = "".join(('<li><a class="nv" href="%s">%s</a></li>' % (k, E(t))) if k.startswith("/") else
                  ('<li><button type="button" class="nv" aria-expanded="false" aria-controls="mega-%s" data-mega="mega-%s">%s'
                   '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button></li>' % (k, k, E(t)))
                  for t, k in nav)
    util = ('<div class="util"><div class="wrap util-in"><p><span class="dot"></span>AI, data and forward deployed engineering for the enterprise</p>'
            '<ul><li><a href="/about/locations">Locations</a></li><li><a href="/about/careers">Careers</a></li><li><a href="/resources">Resource Center</a></li>'
            '<li><a href="/contact">Contact</a></li></ul></div></div>')
    return ('%s<header class="hdr" id="top"><div class="wrap hdr-in"><a class="brand" href="/" aria-label="Prolifics home">'
            '<img class="lg-w" src="assets/prolifics-logo-white.png" alt="Prolifics" width="140" height="21"><img class="lg-c" src="assets/prolifics-logo.png" alt="" width="128" height="44"></a>'
            '<nav aria-label="Main"><ul class="nav">%s</ul></nav><a class="btn btn-c hdr-cta" href="/contact">Talk to Our Experts</a>'
            '<button type="button" class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button></div>'
            '%s%s%s%s</header>' % (util, lis, mega_services(), mega_industries(), mega_resources(), mega_about()))

def drawer():
    def acc(title, inner):
        return '<details class="acc"><summary>%s</summary><div class="acc-b">%s</div></details>' % (E(title), inner)
    svc = "".join(acc(p["name"], '<a class="ov" href="%s">View overview</a>' % p["href"] + "".join(
        '<p class="dh">%s</p>%s' % (E(h), "".join('<a href="%s">%s</a>' % (u, E(t)) for t, u in links)) for h, links in p["groups"])) for p in PRACTICES)
    tech = acc("Technologies", "".join('<p class="dh">%s</p><p class="dt">%s</p>' % (E(h), E(", ".join(cs))) for h, cs in TECH))
    sol = '<a class="ov" href="/solutions">All solutions</a>' + "".join('<p class="dh">%s</p>%s' % (E(g), "".join('<a href="%s">%s</a>' % (u, E(t)) for t, d, u, ic, tl in items)) for g, items in SOLUTIONS)
    ind = '<a class="ov" href="/industries">Explore all industries</a>' + "".join('<a href="%s">%s</a>' % (u, E(t)) for t, d, u, ic, im in INDUSTRIES)
    abt = "".join('<p class="dh">%s</p>%s' % (E(h), "".join('<a href="%s">%s</a>' % (u, E(t)) for t, d, u in links)) for h, links in ABOUT)
    res = "".join('<p class="dh">%s</p>%s' % (E(h), "".join('<a href="%s"%s>%s</a>' % (u, ' rel="noopener"' if u.startswith("http") else "", E(t)) for t, d, u in links)) for h, links in RESOURCES_MENU)
    return ('<div class="drawer" id="drawer" hidden><div class="dr-in"><p class="dh top">Services</p>%s%s%s'
            '<a class="dl" href="/partnerships">Partnerships</a>%s%s'
            '<a class="btn btn-p blk" href="/contact">Talk to Our Experts</a></div></div>'
            % (svc, tech, acc("Industries", ind), acc("Resources", res), acc("About Us", abt)))

# ---------------------------------------------------------------- hero: 48 years
def hero():
    layers = "".join('<span class="n48-l%s" style="background-image:url(assets/img/%s.jpg)" aria-hidden="true">48</span>' % (" on" if i == 0 else "", e[4]) for i, e in enumerate(ERAS))
    washes = "".join('<span class="wash%s" style="background-image:url(assets/img/%s.jpg)"></span>' % (" on" if i == 0 else "", e[4]) for i, e in enumerate(ERAS))
    ticks = "".join('<li><button type="button" class="tk" data-y="%s" data-t="%s" data-d="%s" aria-label="%s, %s"><span class="tk-y">%s</span><span class="tk-bar"><i></i></span></button></li>'
                    % (E(y), E(t), E(d), E(sh), E(y), E(sh)) for i, (y, sh, t, d, im) in enumerate(ERAS))
    y0, sh0, t0, d0, _ = ERAS[0]
    return ('<section class="hero" aria-label="48 years of Prolifics"><div class="aur" aria-hidden="true"><i></i><i></i><i></i></div><div class="washes" aria-hidden="true">%s</div><div class="grain" aria-hidden="true"></div>'
            '<div class="wrap hero-in"><div class="h-top"><p class="h-kick"><span class="h-sep"></span>Celebrating 48 years of enterprise engineering</p></div>'
            '<div class="h-main"><div class="n48" role="img" aria-label="48 years"><span class="n48-o" aria-hidden="true">48</span>%s<span class="n48-y">years</span></div>'
            '<div class="h-copy"><h1>48 years of making enterprise technology work. <em>Now we put AI to work inside it.</em></h1>'
            '<p class="lead">From developer tools in New York to AI agents in production: integration, data, Salesforce, ServiceNow and SAP, '
            'delivered by 2,000+ engineers with forward deployed pods inside your teams.</p>'
            '<div class="ctas"><a class="btn btn-c" href="/contact">Talk to Our Experts</a><a class="btn btn-gl" href="/about">Our 48 year story %s</a></div></div></div>'
            '<div class="era" aria-live="polite"><div class="era-cap"><p class="era-y">%s</p><p class="era-t">%s</p><p class="era-d">%s</p></div>'
            '<ol class="ticks" role="list">%s</ol></div></div></section>'
            % (washes, layers, arrow(), E(y0), E(t0), E(d0), ticks))

LOGO_ASPECT = {}   # filled by the build before rendering: trimmed aspect ratio per client logo

def logo_grid(files, aspect, title, id_="clients", sub=""):
    """Client wall by industry (Mac, 23 Nov 2026): tabs per industry, up to 11 logos plus a 150+ tile, and a starred
    note that clientele spans Prolifics and its group companies. `files` is kept for callers and ignored."""
    from logoutil import size
    def one(i, f):
        h, w = size(aspect.get(f, 3.0)); h, w = round(h * 1.12), round(w * 1.12)
        name = re.sub(r"[-_]", " ", f.rsplit("/", 1)[-1].rsplit(".", 1)[0]).title()
        return ('<li data-r style="transition-delay:%.2fs"><img src="assets/clients/%s" alt="%s" width="%d" height="%d" style="height:%dpx" loading="lazy"></li>'
                % ((i % 6) * 0.05 + (i // 6) * 0.07, f, E(name), w, h, h))
    more = ('<li class="lgw-more" data-r><b>150+</b><span>Fortune 1000 clients across the Prolifics group<sup>*</sup></span></li>')
    tabs = "".join('<button type="button" class="lgw-t%s" role="tab" id="lwt-%s-%s" aria-controls="lwp-%s-%s" aria-selected="%s" tabindex="%d">%s</button>'
                   % (" on" if i == 0 else "", id_, k, id_, k, "true" if i == 0 else "false", 0 if i == 0 else -1, E(t)) for i, (k, t, fs) in enumerate(WALL))
    panels = "".join('<ul class="lgw-g" role="tabpanel" id="lwp-%s-%s" aria-labelledby="lwt-%s-%s"%s>%s%s</ul>'
                     % (id_, k, id_, k, "" if i == 0 else " hidden", "".join(one(j, f) for j, f in enumerate(fs[:11])), more) for i, (k, t, fs) in enumerate(WALL))
    s = '<p class="lgw-s">%s</p>' % E(sub) if sub else ""
    js = ('<script>(function(){var w=document.getElementById("%s");if(!w)return;var t=[].slice.call(w.querySelectorAll(".lgw-t"));'
          'function sel(b,f){t.forEach(function(x){var on=x===b;x.classList.toggle("on",on);x.setAttribute("aria-selected",on);x.tabIndex=on?0:-1;'
          'var p=document.getElementById(x.getAttribute("aria-controls"));p.hidden=!on;if(on)[].forEach.call(p.querySelectorAll("[data-r]"),function(e){e.classList.add("in")});});if(f)b.focus();}'
          't.forEach(function(b,i){b.addEventListener("click",function(){sel(b)});b.addEventListener("keydown",function(e){var j=e.key==="ArrowRight"?(i+1)%%t.length:e.key==="ArrowLeft"?(i-1+t.length)%%t.length:-1;'
          'if(j>-1){e.preventDefault();sel(t[j],1);}});});})();</script>' % id_)
    return ('<section class="lgw" id="%s" aria-label="Selected clients"><div class="wrap"><h2 class="lgw-h" data-r>%s</h2>%s'
            '<div class="lgw-tl" role="tablist" aria-label="Clients by industry">%s</div>%s<p class="lgw-n"><sup>*</sup>%s</p></div>%s</section>'
            % (id_, E(title), s, tabs, panels, E(WALL_NOTE), js))

def group_logo(name, cls="glogo"):
    f = GROUP_LOGO.get(name)
    return '<span class="%s"><img src="assets/group/%s" alt="%s" loading="lazy"></span>' % (cls, f, E(name)) if f else ""

def logos():
    return logo_grid(None, LOGO_ASPECT, "Trusted by 150+ Fortune 1000 clients")

def stats():
    cells = "".join('<div class="st" data-r><p class="st-n" data-count="%s">%s</p><p class="st-l">%s</p><p class="st-d">%s</p></div>'
                    % (n, n, E(l), E(d)) for n, l, d, s, u in STATS)
    return ('<section class="stats"><div class="wrap"><div class="st-h" data-r><h2>Four decades of making complex systems work, and the scale to do it anywhere.</h2></div>'
            '<div class="st-g">%s</div></div></section>' % cells)

def practices():
    rows = []
    for i, p in enumerate(PRACTICES):
        n = sum(len(l) for h, l in p["groups"])
        groups = "".join('<div class="pg"><h4>%s</h4><ul>%s</ul></div>' % (E(h), "".join('<li><a href="%s">%s</a></li>' % (u, E(t)) for t, u in links)) for h, links in p["groups"])
        rows.append('<li class="pr%s" data-img="assets/img/%s.jpg"><button type="button" class="pr-b" aria-expanded="%s" aria-controls="pr-%s">'
                    '<span class="pr-n">%02d</span><span class="pr-t">%s</span><span class="pr-d">%s</span><span class="pr-c">%d services</span><span class="pr-x" aria-hidden="true"></span></button>'
                    '<div class="pr-p" id="pr-%s"%s><div class="pr-in">%s<div class="pr-tx"><p>%s</p><div class="pr-a"><a class="btn btn-p sm" href="%s">Explore %s</a>'
                    '<a class="lnk" href="%s">Start with: %s %s</a></div></div><div class="pgs">%s</div></div></div></li>'
                    % (" open" if i == 0 else "", p["img"], "true" if i == 0 else "false", p["k"], i + 1, E(p["name"]), E(p["desc"]), n, p["k"], "" if i == 0 else " hidden",
                       img(p["img"], "", "pr-im"), E(p["long"]), p["href"], E(p["name"]), p["start"][1], E(p["start"][0]), arrow(), groups))
    return ('<section class="sec" id="services"><div class="wrap"><div class="sh" data-r>%s<h2>Eight practices. One way of delivering: scoped first, measured always.</h2>'
            '<p class="sh-p">Every engagement starts with a defined scope and a measurable first step, then moves to build, run and scale.</p></div>'
            '<ul class="prs">%s</ul></div><div class="cursor-img" aria-hidden="true"><img alt=""></div></section>' % (label("01", "What we do"), "".join(rows)))

def fde():
    pods = "".join('<li><span>%02d</span>%s</li>' % (i + 1, E(t.replace(" Pod", ""))) for i, (t, u) in enumerate(PRACTICES[1]["groups"][0][1]))
    eng = "".join('<li><b>%s</b><span>%s</span></li>' % (E(t), E(d)) for t, d, ic in ENGAGE)
    weeks = "".join('<span>Week %d</span>' % w for w in range(7))
    bars = "".join('<span class="bar b%d"><i></i><em>%s</em></span>' % (i, E(t)) for i, (w, t, d) in enumerate(SPRINT))
    cards = "".join('<li class="spc" data-r><span class="spc-im">%s</span><p class="sp-w">%s</p><p class="sp-t">%s</p><p class="sp-d">%s</p></li>'
                    % (img(SPRINT_IMG[i], ""), E(w), E(t), E(d)) for i, (w, t, d) in enumerate(SPRINT))
    return ('<section class="fde" id="fde"><div class="wrap"><div class="fde-in"><div class="fde-v" data-r>%s<div class="fde-q"><p class="fde-qn">6</p><p>weeks from signed baseline to one AI workflow live in production</p></div></div>'
            '<div class="fde-c">%s<h2 data-r>We don\'t just advise. We build and operationalize.</h2>'
            '<p class="fde-p" data-r>Forward deployed engineering pods embed inside your teams to take AI from pilot to production across data, Salesforce, ServiceNow and SAP. '
            'Small and senior: an onshore lead with the business owner, a deployment strategist, an evaluation engineer and an engineering squad.</p>'
            '<p class="sp-h">Six pods</p><ul class="pods" data-r>%s</ul>'
            '<p class="sp-h">Ways to engage</p><ul class="engs" data-r>%s</ul><a class="btn btn-c" href="/services/fde-ai-engineering">Explore FDE AI Engineering %s</a></div></div>'
            '<div class="spr"><div class="spr-h" data-r><p class="sp-h">How a sprint runs</p><h3>Six weeks, four moves, one workflow in production</h3></div>'
            '<div class="spr-ruler" data-r aria-hidden="true"><div class="spr-wk">%s</div><div class="spr-bars">%s</div></div>'
            '<ol class="spr-cards">%s</ol></div></div></section>'
            % (img("fde_team", "A small senior team working closely together"), label("02", "FDE AI Engineering", True), pods, eng, arrow(), weeks, bars, cards))

def solutions():
    slug = lambda g: re.sub(r"\W+", "-", g.lower())
    chips = ['<button type="button" class="fc on" data-f="all" aria-pressed="true">All 16</button>'] + [
        '<button type="button" class="fc" data-f="%s" aria-pressed="false">%s</button>' % (slug(g), E(g)) for g, it in SOLUTIONS]
    cards, n = [], 0
    for g, items in SOLUTIONS:
        for k, (t, d, u, ic, tl) in enumerate(items):
            im = SOL_CARD_IMG[n]; n += 1
            cards.append('<a class="sc" href="%s" data-g="%s"><span class="sc-im" style="background-image:url(assets/img/%s.jpg);background-position:%d%% 50%%"></span>'
                         '<span class="sc-b"><span class="sc-g">%s</span><h3>%s</h3><p>%s</p><span class="sc-f"><span class="sc-tl">%s</span><span class="sc-x">Explore %s</span></span></span></a>'
                         % (u, slug(g), im, 50, E(g), E(t), E(d), E(tl) if tl else "Scoped on discovery", arrow()))
    return ('<section class="sec sol" id="solutions"><div class="wrap"><div class="sh" data-r>%s<h2>Packaged solutions with a clear scope, timeline and first step</h2>'
            '<div class="sh-r"><div class="rail-n"><button type="button" class="rn" data-d="-1" aria-label="Previous solutions">%s</button><button type="button" class="rn" data-d="1" aria-label="Next solutions">%s</button></div>'
            '<a class="lnk" href="/solutions">View all solutions %s</a></div></div><div class="fcs" role="group" aria-label="Filter solutions">%s</div></div>'
            '<div class="sc-rail" tabindex="0" aria-label="Solutions">%s</div></section>'
            % (label("03", "Solutions"), arrow(), arrow(), arrow(), "".join(chips), "".join(cards)))

def proof():
    def card(c, i):
        f, client, sector, by, title, brief, m, ml, im, u = c
        return ('<article class="cs%s" tabindex="0" aria-label="%s case study"><img class="cs-im" src="assets/img/%s.jpg" alt="" loading="lazy"><span class="cs-sh"></span>'
                '<div class="cs-in"><img class="cs-lg" src="assets/clients/%s" alt="%s"><div class="cs-body"><p class="cs-k">%s<span>Delivered by %s</span></p><h3>%s</h3><p class="cs-d">%s</p>'
                '<div class="cs-f"><div class="cs-m"><b data-count="%s">%s</b><span>%s</span></div><a class="cs-btn" href="%s" rel="noopener">Read the case study %s</a></div></div></div></article>'
                % (" on" if i == 0 else "", E(client), im, f, E(client), E(sector), E(by), E(title), E(brief), m, E(m), E(ml), u, arrow()))
    def text(c):
        f, client, sector, by, title, brief, m, ml, im, u = c
        return ('<a class="pc" href="%s" rel="noopener" data-r><div class="pc-l"><img src="assets/clients/%s" alt="%s" loading="lazy"></div>'
                '<p class="pc-m" data-count="%s">%s</p><p class="pc-ml">%s</p><h3>%s</h3><p class="pc-b">%s</p>'
                '<p class="pc-f"><span>%s</span><span>Delivered by %s</span></p><span class="pc-x">Read the case study %s</span></a>'
                % (u, f, E(client), m, E(m), E(ml), E(title), E(brief), E(sector), E(by), arrow()))
    feat = '<div class="cs-row feat" data-r>%s</div>' % "".join(card(c, i) for i, c in enumerate(CASES[:3]))
    rest = '<div class="pc-g pc-more">%s</div>' % "".join(text(c) for c in CASES[3:])
    return ('<section class="sec proof" id="proof"><div class="wrap"><div class="sh" data-r>%s<h2>Measured results for enterprises that cannot afford downtime</h2>'
            '<p class="sh-p">Published work from Prolifics and its group companies, across health, finance, government and industry.</p></div>%s%s</div></section>'
            % (label("03", "Case studies"), feat, rest))

def industries():
    tiles = "".join('<a class="it it%d" href="%s" data-r>%s<span class="it-c"><b>%s</b><small>%s</small><span class="it-x">Explore %s</span></span></a>'
                    % (i, u, img(im, ""), E(t), E(d), arrow()) for i, (t, d, u, ic, im) in enumerate(INDUSTRIES))
    return ('<section class="sec" id="industries"><div class="wrap"><div class="sh" data-r>%s<h2>Industry-focused solutions powered by innovation</h2>'
            '<a class="lnk" href="/industries">Explore all industries %s</a></div><div class="it-g">%s</div></div></section>' % (label("04", "Industries"), arrow(), tiles))

def platforms():
    half = len(PARTNERS) // 2
    row = lambda ps: "".join('<a href="/partnerships#partner-%s">%s</a>' % (re.sub(r"\W+", "-", p.lower()), E(p)) for p in ps)
    r1, r2 = row(PARTNERS[:half]), row(PARTNERS[half:])
    tech = "".join('<div class="tg"><h4>%s</h4><p>%s</p></div>' % (E(h), E(", ".join(cs))) for h, cs in TECH)
    return ('<section class="sec plat" id="platforms"><div class="wrap"><div class="sh" data-r>%s<h2>Strategic technology partnerships</h2>'
            '<a class="lnk" href="/partnerships">View all partnerships %s</a></div></div>'
            '<div class="tmq"><div class="tmq-r"><div class="tmq-t">%s</div><div class="tmq-t" aria-hidden="true">%s</div></div>'
            '<div class="tmq-r rev"><div class="tmq-t">%s</div><div class="tmq-t" aria-hidden="true">%s</div></div></div>'
            '<div class="wrap"><div class="tgs" data-r>%s</div></div></section>' % (label("05", "Partnerships"), arrow(), r1, r1, r2, r2, tech))

def group():
    g = "".join('<li>%s<span>%s</span></li>' % (group_logo(t, "glogo d"), E(d)) for t, d, ic in GROUP)
    off = "".join('<li><b>%s</b><span>%s</span></li>' % (E(r), E(c)) for r, c in OFFICES)
    return ('<section class="grp" id="about">%s<div class="wrap grp-in"><div class="grp-l" data-r>%s<h2>One group, one account team, global delivery</h2>'
            '<p class="grp-p">Specialist firms brought together under one name, so a client works with one team across platforms, testing and data.</p>'
            '<ul class="gl">%s</ul><a class="lnk lnk-l" href="/group" style="margin-top:22px">Meet the group companies %s</a></div><div class="grp-r" data-r><p class="grp-k"><span class="big">13</span>offices in 6 countries</p><ul class="ol">%s</ul>'
            '<a class="lnk lnk-l" href="/about/locations">All locations %s</a></div></div></section>'
            % (img("globe", "Earth at night with city lights", "grp-bg"), label("06", "Why Prolifics", True), g, arrow(), off, arrow()))

def guides():
    cards = "".join('<a class="gd" href="%s" data-r><span class="gd-im">%s</span><span class="gd-k">Planning guide</span><h3>%s</h3><p>%s</p><span class="lnk">Read the guide %s</span></a>'
                    % (u, img(im, ""), E(t), E(d), arrow()) for t, d, u, im in GUIDES)
    return ('<section class="sec" id="insights"><div class="wrap"><div class="sh" data-r>%s<h2>Enterprise AI planning guides</h2>'
            '<p class="sh-p">Practical questions to answer before choosing a delivery model, preparing data or releasing an agent.</p></div><div class="gd-g">%s</div></div></section>'
            % (label("07", "Insights"), cards))

def cta():
    return ('<section class="cta">%s<div class="wrap cta-in" data-r><p class="cta-k">The next 48 years start with one workflow</p><h2>Bring one process. Leave with it in production.</h2>'
            '<p class="cta-p">Tell us the process, the platform and the result you need. We will come back with a scoped first step, the team, and how we will measure it.</p>'
            '<div class="ctas"><a class="btn btn-c" href="/contact">Talk to Our Experts</a><a class="btn btn-gl" href="/services">Explore services %s</a></div></div></section>'
            % (img("cta", "", "cta-bg"), arrow()))

def footer():
    cols = "".join('<div class="fc-c"><h4>%s</h4><ul>%s</ul></div>' % (E(h), "".join('<li><a href="%s">%s</a></li>' % (u, E(t)) for t, u in links)) for h, links in FOOTER)
    legal = "".join('<li><a href="%s">%s</a></li>' % (u, E(t)) for t, u in LEGAL)
    return ('<footer class="ftr"><div class="wrap"><div class="ftr-big" aria-hidden="true">Vision to Value<span>.</span></div><div class="ftr-t"><div class="ftr-b">'
            '<img src="assets/prolifics-logo-white.png" alt="Prolifics" width="150" height="23"><p>AI, data and forward deployed engineering for the enterprise. Founded in New York in 1978.</p>'
            '<p class="ftr-o">New York, Westbury, Trevose, Orlando, Toronto, London, Borehamwood, Stevenage, Hamburg, Dubai, Hyderabad, Pune</p>'
            '<a class="btn btn-c sm" href="/contact">Talk to Our Experts</a></div>%s</div>'
            '<div class="ftr-l"><p>&copy; 2026 Prolifics. All rights reserved.</p><ul>%s</ul></div></div></footer>' % (cols, legal))

CSS = (open(os.path.join(HERE, "home.css"), encoding="utf-8").read() + open(os.path.join(HERE, "home-v4.css"), encoding="utf-8").read()
       + open(os.path.join(HERE, "standing.css"), encoding="utf-8").read() + open(os.path.join(HERE, "palette.css"), encoding="utf-8").read() + open(os.path.join(HERE, "logogrid.css"), encoding="utf-8").read())

def standing():
    import standing as S
    return S.section(img, arrow, '<p class="lab"><span>IBM + SAP</span>Partner credentials</p>', "v1")
JS = open(os.path.join(HERE, "home.js"), encoding="utf-8").read()

def page(final=False):
    robots = "" if final else '<meta name="robots" content="noindex, nofollow">'
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": "Prolifics", "url": "https://prolifics.ai/", "foundingDate": "1978",
          "foundingLocation": "New York", "description": "AI, data and forward deployed engineering for the enterprise across data platforms, Salesforce, ServiceNow and SAP."}
    preload = '<link rel="preload" as="image" href="assets/img/%s.jpg">' % ERAS[0][4]
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">%s%s'
            '<title>Prolifics | AI, Data & Forward Deployed Engineering</title>'
            '<meta name="description" content="48 years of making enterprise technology work. Prolifics builds and runs AI across data platforms, Salesforce, ServiceNow and SAP, with forward deployed engineering pods.">'
            '<script>document.documentElement.className+=" js"</script><meta name="theme-color" content="#FBFAF7"><link rel="icon" href="assets/favicon.png">%s<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
            '<style>%s</style><script type="application/ld+json">%s</script></head><body class="top">%s'
            '<a class="skip" href="#main">Skip to content</a>%s%s<main id="main">%s%s%s%s%s%s%s%s%s%s%s</main>%s<script>%s</script></body></html>'
            % (GTM_HEAD, robots, preload, CSS, json.dumps(ld), GTM_BODY, header(), drawer(), hero(), logos(), stats() + standing(), practices(), fde(), proof(), industries(),
               platforms(), group(), guides(), cta(), footer(), JS))

def copy_images():
    src, dst = os.path.join(HERE, "img2"), os.path.join(DIST, "assets", "img")
    os.makedirs(dst, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if not f.endswith(".jpg"): continue
        im = Image.open(os.path.join(src, f)).convert("RGB")
        mw = 2000 if f.startswith("e") or f in ("cta.jpg", "globe.jpg", "team2.jpg") else 1400
        if im.width > mw: im = im.resize((mw, round(im.height * mw / im.width)), Image.LANCZOS)
        im.save(os.path.join(dst, f), quality=76, optimize=True, progressive=True)

if __name__ == "__main__":
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "assets", "clients"))
    shutil.copy(os.path.join(GTM, "Prolifics-logo-2025.png"), os.path.join(DIST, "assets", "prolifics-logo.png"))
    shutil.copy(os.path.join(GTM, "prolifics-logo-white.png"), os.path.join(DIST, "assets", "prolifics-logo-white.png"))
    shutil.copy(os.path.join(GTM, "favicon.png"), os.path.join(DIST, "assets", "favicon.png"))
    from logoutil import prep
    for f in set(LOGOS + [s[0] for s in STORIES] + [c[0] for c in CASES]):
        LOGO_ASPECT[f] = prep(os.path.join(GTM, "clients", f), os.path.join(DIST, "assets", "clients", f))
    for k, t, fs in WALL:   # industry client wall, including logos published by group companies
        for f in fs:
            if f not in LOGO_ASPECT:
                os.makedirs(os.path.dirname(os.path.join(DIST, "assets", "clients", f)), exist_ok=True)
                LOGO_ASPECT[f] = prep(os.path.join(GTM, "clients", f), os.path.join(DIST, "assets", "clients", f))
    os.makedirs(os.path.join(DIST, "assets", "group"), exist_ok=True)
    for f in GROUP_LOGO.values():
        prep(os.path.join(GTM, "group", f), os.path.join(DIST, "assets", "group", f))
    for f in ("ibm.svg", "sap.svg"):   # partner logos used by the IBM and SAP standing section
        prep(os.path.join(HERE, "partners", f), os.path.join(DIST, "assets", "partners", f))
    from optimize import optimize
    out, n_img, img_bytes = optimize(page("--noindex" not in sys.argv), os.path.join(HERE, "img2"), os.path.join(DIST, "assets", "img"))
    out = out.replace('href="assets/img/e1978.webp"', 'href="assets/img/e1978.webp"')
    import links as L
    out = L.delink(out); L.check(out, "/")
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(out)
    print("images %d, %.0f KB" % (n_img, img_bytes / 1024))
    paths = ["/services/:p*", "/solutions/:p*", "/solutions", "/industries/:p*", "/industries", "/about/:p*", "/about",
             "/partnerships", "/resources/:p*", "/resources", "/contact"]
    vc = {"headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}],
          "redirects": [{"source": p, "destination": "https://prolifics-website.vercel.app" + p, "permanent": False} for p in paths]}
    json.dump(vc, open(os.path.join(DIST, "vercel.json"), "w"), indent=1)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S)
    vis = re.sub(r"<[^>]+>", " ", text)
    print("bytes %d, em/en dashes %d, exclamation %d" % (len(out), len(re.findall("[–—]", text)) + text.count("&mdash;") + text.count("&ndash;"), vis.count("!")))
