# -*- coding: utf-8 -*-
"""Second version of the Prolifics home page in the Kyndryl pattern, Prolifics brand. Builds into ../dist-k.
Run: python3 src/build_k.py   Reuses the menu, drawer and footer from build_home.py."""
import os, re, shutil, json, sys
from PIL import Image
import build_home as H
from build_home import E, img, arrow, header, drawer, footer
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DIST = os.path.join(PROJ, "dist-k")
GTM = H.GTM

LEADERS = [  # names and titles from prolifics.ai/leadership; photos are the official files from that page
    ("satya-bolli-2.png", "Satya Bolli", "Chairman and Managing Director"),
    ("Greg-1.png", "Greg Hodgkinson", "Chief Technology Officer"),
    ("Biju-Nair.webp", "Biju S. Nair", "Global CFO and Head of UK Operations"),
    ("chetan-1.png", "Chetan", "Sales Head"),
    ("ravi-1.png", "Ravi Thalluri", "Head of Operational Excellence"),
    ("Kalyan-Ganjam.png", "Kalyan Ganjam", "Head of Engineering"),
    ("Rakhesh-1.png", "Rakesh Kurchkulla", "Head of Global Delivery"),
]
SATYA_QUOTE = ("Since 1978, our journey has been powered by one belief: technology is most powerful when it is deeply human, "
               "when it serves people, elevates possibilities, and builds lasting trust.")

NEWS = [
    ("Event", "The Prolifics GCC Conclave, December 2026: leaders of global capability centers on building AI ready teams", "Register your interest", "/contact"),
    ("Acquisition", "Prolifics acquires Castaliaz to strengthen global SAP capabilities", "Read the announcement",
     "https://www.dbta.com/Editorial/News-Flashes/Prolifics-Acquires-Castaliaz-to-Strengthen-Global-SAP-Capabilities-171579.aspx"),
    ("Recognition", "Prolifics receives the 2025 IBM North America Sustainability Award", "Our story", "/about"),
]
RECOG = [  # listed on prolifics.ai/about-us
    ("2025 IBM North America Sustainability Award", "IBM", "/about"),
    ("2025 AI-Powered Digital Transformation Award at the 16th Shared Services Summit", "Shared Services Summit", "/about"),
    ("2019 IBM Beacon Award for Outstanding Analytics Solution", "IBM", "/about"),
    ("150+ Fortune 1000 clients across regulated and asset-intensive industries", "Client trust", "/industries"),
]
HELPS = [
    ("Prove value fast", "Scoped assessments, proofs of value and six week sprints that end in a measured result, not a slide.", "Business Transformation", "/services/business-transformation"),
    ("Build on the platforms you run", "Salesforce, ServiceNow, SAP and custom applications, implemented, integrated and governed.", "Explore our services", "/services/salesforce"),
    ("Engineer data for AI", "AI-ready data platforms, analytics, MLOps and governance, with responsible AI built in from day one.", "AI & Data", "/services/ai-services"),
    ("Run and assure", "Managed services, AgentOps and AI test automation that keep releases fast and agents safe.", "Quality Engineering", "/services/qa"),
]
FAQ = [
    ("What does Prolifics do?", "Prolifics builds and runs AI across the systems enterprises already depend on: data platforms, Salesforce, ServiceNow and SAP, plus application, cloud, integration and quality engineering."),
    ("What is forward deployed engineering?", "Small, senior pods embed with the business owner and take one AI workflow from pilot to production in about six weeks, measured against a signed baseline, then hand it over or run it."),
    ("Which platforms do your engineers work on?", "Salesforce, Agentforce, Data 360, MuleSoft, ServiceNow, SAP S/4HANA and BTP, Microsoft, AWS, Google Cloud, IBM watsonx, Databricks, Snowflake and more."),
    ("Where does Prolifics deliver from?", "Thirteen offices in six countries: the United States, Canada, the United Kingdom, Germany, the UAE and India, with engineering and delivery centers in Hyderabad and Pune."),
    ("Which companies are part of the Prolifics group?", "Enable Consulting for Salesforce, Castaliaz for SAP, Prolifics Testing for quality engineering, and Tier 2 Consulting in the UK."),
    ("How does an engagement start?", "With a scoped first step: an assessment, readiness check or sprint with a fixed scope, a named team and a measurable result."),
]

def wm(t):
    return '<div class="wm" aria-hidden="true">%s</div>' % E(t)

def hero():
    def banner(bg, kick, h1, body, cta, href, extra=""):
        return ('<div class="sl">%s<div class="wrap sl-in"><div class="sl-tx"><p class="kk">%s</p><h1>%s</h1>%s'
                '<a class="kbtn" href="%s"%s>%s %s</a></div>%s</div></div>'
                % (bg, E(kick), E(h1), body, href, ' rel="noopener"' if href.startswith("http") else "", E(cta), arrow(), extra))
    photo = lambda name, alt: '<div class="sl-bg">%s</div>' % img(name, alt)
    slides = [
        banner('<div class="sl-bg sat-bg"></div>', "Celebrating 48 years", "Technology is most powerful when it is deeply human.",
               '<p class="sl-by"><b>Satya Bolli</b>Chairman and Managing Director, Prolifics</p>', "Read our 48 year story", "/about",
               '<div class="sat-wrap" aria-hidden="false"><span class="arc"></span>'
               '<img class="sat" src="assets/people/satya-bolli-2.png" alt="Satya Bolli, Chairman and Managing Director of Prolifics"></div>'),
        banner(photo("e2026", "Wooden chess pieces on a board"), "Forward deployed engineering", "One AI workflow. Six weeks. Live in production.",
               '<p class="sl-p">Small senior pods embed with your business owner and take AI from pilot to production on Salesforce, ServiceNow, SAP and your data.</p>',
               "See how a sprint runs", "/services/fde-ai-engineering"),
        banner(photo("k_conf", "A full conference hall"), "The Prolifics GCC Conclave, December 2026", "Where global capability centers decide what AI ready means.",
               '<p class="sl-p">Ten to fifteen GCC leaders on stage, enterprise CxOs in the room, and Satya Bolli among the speakers.</p>', "Register your interest", "/contact"),
        banner(photo("cs_horizon", "A clinician completing a medical form"), "Client results", "60 million claims a year, handled automatically.",
               '<p class="sl-p">Horizon Blue Cross Blue Shield of New Jersey runs claims through automated handling built by Prolifics, so examiners spend their time on the exceptions.</p>',
               "Read the case study", "https://www.casestudies.com/company/prolifics/case-study/horizon-improves-the-health-of-claims-processes-with-bpm"),
        banner(photo("e1978", "A computer room from the mainframe era"), "Since 1978", "From mainframes to AI agents, we make enterprise technology work.",
               '<p class="sl-p">48 years, 2,000+ experts and 13 offices in 6 countries, with forward deployed pods inside your teams.</p>', "Our story", "/about"),
    ]
    dots = "".join('<button type="button" class="kdot" aria-label="Show banner %d"><i></i></button>' % (i + 1) for i in range(len(slides)))
    news = "".join('<a class="nw" href="%s"%s><span class="nw-k">%s</span><span class="nw-t">%s</span><span class="nw-l">%s %s</span></a>'
                   % (u, ' rel="noopener"' if u.startswith("http") else "", E(k), E(t), E(l), arrow()) for k, t, l, u in NEWS)
    return ('<section class="khero" aria-roledescription="carousel" aria-label="Featured"><div class="trk">%s</div>'
            '<div class="wrap kh-ui"><span class="cnt">01 / %02d</span><div class="dots">%s</div>'
            '<div class="arws"><button type="button" class="arw prev" aria-label="Previous banner">%s</button>'
            '<button type="button" class="arw next" aria-label="Next banner">%s</button></div></div></section>'
            '<section class="news"><div class="wrap news-g">%s</div></section>' % ("".join(slides), len(slides), dots, arrow(), arrow(), news))

def jump():
    items = [("Who we are", "#who"), ("Client stories", "#stories"), ("How we help", "#help"), ("Our people", "#people"), ("FAQ", "#faq")]
    return '<nav class="jump" aria-label="On this page"><div class="jump-in">%s</div></nav>' % "".join('<a href="%s">%s</a>' % (u, E(t)) for t, u in items)

def who():
    return ('<section class="who" id="who"><div class="wrap who-in"><div class="who-tx" data-r><p class="kk dk">Who we are</p>'
            '<h2>Where 48 years of engineering meets AI in production</h2><p>We help enterprises in every industry make their essential systems work, and now put AI to work inside them. '
            'Steady operations are not enough: Prolifics brings the engineers, platforms and proven delivery patterns that move AI from a pilot to a measured result.</p>'
            '<div class="who-l"><a href="/about">Our story</a><a href="/about/leadership">Leadership</a><a href="/about/locations">Locations</a></div></div>'
            '<a class="who-blk" href="/about" data-r><span>We are Prolifics</span><em>2,000+ experts, 13 offices, 6 countries %s</em></a></div></section>' % arrow())

def recog():
    panes = "".join('<button type="button" class="rc%s" aria-expanded="%s"><span class="rc-n">%02d</span><span class="rc-t">%s</span><span class="rc-s">%s</span></button>'
                    % (" on" if i == 0 else "", "true" if i == 0 else "false", i + 1, E(t), E(s)) for i, (t, s, u) in enumerate(RECOG))
    return ('<section class="recog"><div class="wrap recog-in"><div class="recog-h" data-r><h2>Industry recognition.<br><em>Client trust.</em></h2>'
            '<p>Awards as listed by Prolifics, and the clients who keep coming back.</p></div><div class="rc-row" data-r>%s</div></div></section>' % panes)

def stories():
    items = CASES[:3]
    slides = "".join('<div class="st-sl%s"><img src="assets/img/%s.jpg" alt="" loading="lazy"><div class="st-cap"><img class="st-lg" src="assets/clients/%s" alt="%s">'
                     '<p class="kk">%s</p><h3>%s</h3><p class="st-m"><b>%s</b> %s</p><a class="kbtn sm" href="%s" rel="noopener">Read full story %s</a></div></div>'
                     % (" on" if i == 0 else "", im, f, E(client), E(sector), E(title), E(m), E(ml), u, arrow())
                     for i, (f, client, sector, by, title, brief, m, ml, im, u) in enumerate(items))
    tabs = "".join('<button type="button" class="st-tb%s"><span>%02d</span><i></i></button>' % (" on" if i == 0 else "", i + 1) for i in range(len(items)))
    return ('<section class="stories" id="stories">%s<div class="wrap"><div class="sec-h" data-r><h2>Progress, one client at a time</h2>'
            '<p>We work hand in hand with clients and partners to run and transform their essential systems.</p></div>'
            '<div class="st-wrap" data-r>%s</div><div class="st-tabs">%s</div></div></section>' % (wm("client stories"), slides, tabs))

def helps():
    cols = "".join('<div class="hp" data-r><p class="hp-n">%02d</p><h3>%s</h3><p>%s</p><a href="%s">%s %s</a></div>' % (i + 1, E(t), E(d), u, E(l), arrow())
                   for i, (t, d, l, u) in enumerate(HELPS))
    return ('<section class="helps" id="help">%s<div class="wrap"><div class="sec-h" data-r><h2>Continuous innovation<br>+ engineering you can run</h2></div>'
            '<div class="hp-g">%s</div></div></section>' % (wm("how we help"), cols))

def aiband():
    return ('<section class="aib"><div class="wrap aib-in" data-r><div class="aib-im">%s</div><div class="aib-tx"><h2>Put AI to work inside the platforms you already run</h2>'
            '<p>Forward deployed pods build one workflow at a time, measure it against a baseline, then hand it over or run it for you.</p>'
            '<a class="lnk" href="/services/fde-ai-engineering">Get started with FDE AI Engineering %s</a></div></div></section>' % (img("k_relay", "A relay baton being handed over"), arrow()))

def insights():
    cards = "".join('<a class="in-c" href="%s" data-r><span class="in-im">%s</span><span class="kk dk">Planning guide</span><h3>%s</h3><p>%s</p><span class="in-l">Read the guide %s</span></a>'
                    % (u, img(im, ""), E(t), E(d), arrow()) for t, d, u, im in GUIDES)
    return ('<section class="ins"><div class="wrap"><div class="sec-h" data-r><p class="kk dk">Trends and insights</p><h2>Ideas that move AI from pilot to production</h2></div>'
            '<div class="in-g">%s</div></div></section>' % cards)

def band():
    return ('<section class="band"><div class="wrap band-in" data-r><h2>Delivering resilient, outcome focused engineering for complex enterprise estates</h2>'
            '<div class="band-r"><p><b>2,000+</b>experts</p><p><b>13</b>offices</p><p><b>6</b>countries</p><a href="/about/locations">Where we work %s</a></div></div></section>' % arrow())

def people():
    s = LEADERS[0]
    others = "".join('<div class="ld" data-r><span class="ld-im"><img src="assets/people/%s" alt="%s" loading="lazy"></span><b>%s</b><span>%s</span></div>'
                     % (f, E(n), E(n), E(t)) for f, n, t in LEADERS[1:])
    return ('<section class="people" id="people">%s<div class="wrap"><div class="sec-h" data-r><h2>Trusted. Experienced. Skilled.</h2>'
            '<p>People are the strength of Prolifics. For 48 years they have used deep domain knowledge and relentless curiosity to design, build and run what enterprises depend on.</p></div>'
            '<div class="spot" data-r><div class="spot-im"><img src="assets/people/%s" alt="%s"></div><div class="spot-tx"><p class="kk dk">A word from our chairman</p>'
            '<blockquote>%s</blockquote><p class="spot-by"><b>%s</b>%s</p><a class="kbtn dk" href="/about/leadership">Meet the leadership team %s</a></div></div>'
            '<div class="ld-g">%s</div></div></section>' % (wm("our people"), s[0], E(s[1]), E(SATYA_QUOTE), E(s[1]), E(s[2]), arrow(), others))

PARTNER_LOGOS = [("IBM", "ibm.svg"), ("Salesforce", "salesforce.svg"), ("ServiceNow", "servicenow.svg"), ("SAP", "sap.svg"), ("Microsoft", "microsoft.svg"),
                 ("Boomi", "boomi.svg"), ("AWS", "aws.svg"), ("MuleSoft", "mulesoft.svg"), ("Databricks", "databricks.png"), ("Red Hat", "red-hat.svg"),
                 ("Snowflake", "snowflake.png"), ("Google Cloud", "google-cloud.png"), ("EDB", "edb.png"), ("Tricentis", "tricentis.png")]
PARTNER_ASPECT = {}

def partners():
    from logoutil import size
    def cell(n, f):
        h, w = size(PARTNER_ASPECT.get(f, 3.0), base=56, lo=22, hi=46, maxw=150)
        return ('<a href="/partnerships#partner-%s"><img src="assets/partners/%s" alt="%s" width="%d" height="%d" style="height:%dpx" loading="lazy"><span>%s</span></a>'
                % (re.sub(r"\W+", "-", n.lower()), f, E(n), w, h, h, E(n)))
    return ('<section class="parts"><div class="wrap"><div class="sec-h" data-r><h2>Trusted by our technology partners</h2>'
            '<a class="lnk" href="/partnerships">Learn more about partnerships %s</a></div>'
            '<div class="pt-g" data-r>%s</div></div></section>' % (arrow(), "".join(cell(n, f) for n, f in PARTNER_LOGOS)))

def careers():
    return ('<section class="car"><div class="wrap"><h2 class="car-h" data-r>Build what comes next with us</h2><div class="car-g" data-r>'
            '<div class="car-im">%s</div><div class="car-blk"><p class="kk">Careers</p><h3>Join 2,000+ engineers, consultants and builders</h3>'
            '<p>Work on Salesforce, ServiceNow, SAP, data and AI programs for enterprises across North America, Europe, the Middle East and India.</p>'
            '<a class="kbtn" href="/about/careers">Explore jobs %s</a></div></div></div></section>' % (img("k_summit", "A climbing team on a mountain ridge"), arrow()))

def faq():
    qs = "".join('<details class="fq"%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", E(q), E(a)) for i, (q, a) in enumerate(FAQ))
    return ('<section class="faq" id="faq"><div class="wrap faq-in"><h2 data-r>Answers to questions about Prolifics</h2><div class="fq-l" data-r>%s</div></div></section>' % qs)

KCSS = (open(os.path.join(HERE, "k.css"), encoding="utf-8").read() + open(os.path.join(HERE, "k-hero.css"), encoding="utf-8").read()
        + open(os.path.join(HERE, "standing.css"), encoding="utf-8").read())

def standing():
    import standing as S
    return S.section(img, arrow, '<p class="kk dk">Partner credentials</p>', "k")
KJS = open(os.path.join(HERE, "k.js"), encoding="utf-8").read()

def page(final=False):
    robots = "" if final else '<meta name="robots" content="noindex, nofollow">'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">%s'
            '<title>Prolifics | AI, Data & Forward Deployed Engineering</title>'
            '<meta name="description" content="48 years of making enterprise technology work. Prolifics builds and runs AI across data platforms, Salesforce, ServiceNow and SAP.">'
            '<script>document.documentElement.className+=" js"</script><link rel="icon" href="assets/favicon.png">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
            '<style>%s%s</style></head><body class="kpage"><a class="skip" href="#main">Skip to content</a>%s%s<main id="main">%s%s%s%s%s%s%s%s%s%s%s%s%s%s</main>%s'
            '<script>%s</script><script>%s</script></body></html>'
            % (robots, H.CSS, KCSS, header(), drawer(), hero(), jump(), who() + standing(), recog(), stories(), helps(), aiband(), insights(), band(), people(), partners(),
               careers(), faq(), "", footer(), H.JS, KJS))

if __name__ == "__main__":
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "assets", "clients")); os.makedirs(os.path.join(DIST, "assets", "img")); os.makedirs(os.path.join(DIST, "assets", "people"))
    for f, n, t in LEADERS:
        im = Image.open(os.path.join(HERE, "people", f)).convert("RGBA")
        im.save(os.path.join(DIST, "assets", "people", f.rsplit(".", 1)[0] + ".webp"), "WEBP", quality=80, method=6)
    for f in ["Prolifics-logo-2025.png", "prolifics-logo-white.png", "favicon.png"]:
        shutil.copy(os.path.join(GTM, f), os.path.join(DIST, "assets", {"Prolifics-logo-2025.png": "prolifics-logo.png"}.get(f, f)))
    from logoutil import prep
    for f in set(LOGOS + [c[0] for c in CASES]):
        prep(os.path.join(GTM, "clients", f), os.path.join(DIST, "assets", "clients", f))
    for n, f in PARTNER_LOGOS:
        PARTNER_ASPECT[f] = prep(os.path.join(HERE, "partners", f), os.path.join(DIST, "assets", "partners", f))
    from optimize import optimize
    out = re.sub(r"assets/people/([\w-]+)\.(?:png|webp)", r"assets/people/\1.webp", page("--final" in sys.argv))
    out, n_img, img_bytes = optimize(out, os.path.join(HERE, "img2"), os.path.join(DIST, "assets", "img"))
    print("images %d, %.0f KB" % (n_img, img_bytes / 1024))
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(out)
    paths = ["/services/:p*", "/solutions/:p*", "/solutions", "/industries/:p*", "/industries", "/about/:p*", "/about", "/partnerships", "/resources/:p*", "/resources", "/contact"]
    vc = {"headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}],
          "redirects": [{"source": p, "destination": "https://prolifics-website.vercel.app" + p, "permanent": False} for p in paths]}
    json.dump(vc, open(os.path.join(DIST, "vercel.json"), "w"), indent=1)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S); vis = re.sub(r"<[^>]+>", " ", text)
    print("bytes %d, em/en dashes %d, exclamation %d" % (len(out), len(re.findall("[–—]", text)), vis.count("!")))
