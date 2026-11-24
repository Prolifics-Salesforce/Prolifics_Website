# -*- coding: utf-8 -*-
"""Five page deck: website platform, domain, new vs existing site, GCC Conclave. Arial, Prolifics brand, white template.
Output: out/Prolifics Website and GCC Conclave - Decisions.pdf (and .html). Facts and sources: research.md (19 Nov 2026)."""
import os, subprocess, html, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
E = lambda s: html.escape(s)
IMG = lambda f: "file://" + os.path.join(HERE, "img", f)
NAME = "Prolifics Website and GCC Conclave - Decisions"

CSS = """
@page{size:1280px 720px;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,Helvetica,sans-serif;color:#0A1226;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.s{position:relative;width:1280px;height:720px;overflow:hidden;page-break-after:always;background:#fff}
.hd{position:absolute;top:0;left:0;right:0;height:62px;display:flex;align-items:center;justify-content:space-between;padding:0 56px;border-bottom:1px solid #E4E8F0}
.hd img{height:30px}.hd span{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6B7690;font-weight:bold}
.ft{position:absolute;bottom:0;left:0;right:0;height:38px;display:flex;align-items:center;justify-content:space-between;padding:0 56px;border-top:1px solid #EEF1F6;font-size:10px;color:#9AA3B8}
.ft .src{max-width:1040px;line-height:1.3}
.bd{position:absolute;top:84px;left:56px;right:56px;bottom:52px}
.eb{font-size:12px;letter-spacing:2.2px;text-transform:uppercase;color:#0077B6;font-weight:bold;display:flex;align-items:center;gap:10px}
.eb:before{content:"";width:22px;height:3px;background:#00AEEF}
h1{font-size:30px;line-height:1.15;letter-spacing:-.4px;margin:8px 0 6px;max-width:1100px}
.sub{font-size:15px;color:#4A5570;max-width:980px;line-height:1.45}
.g{display:grid;gap:14px}
.card{background:#F4F7FC;padding:18px 20px;border-radius:6px}
.card h3{font-size:16px;margin:10px 0 6px}.card p{font-size:13px;color:#3A4560;line-height:1.45}
.n{font-size:13px;font-weight:bold;color:#fff;background:#001F5B;border-radius:50%;width:28px;height:28px;display:inline-flex;align-items:center;justify-content:center}
.stat .big,.big{font-size:44px;font-weight:bold;color:#001F5B;letter-spacing:-1px;line-height:1}
.big small{font-size:18px;color:#0077B6;margin-left:4px}
.stat p{font-size:13px;color:#3A4560;margin-top:6px;line-height:1.4}
.k{font-size:11px;letter-spacing:1.6px;text-transform:uppercase;font-weight:bold;color:#6B7690;margin-bottom:10px}
ul{list-style:none}ul.l li{position:relative;padding-left:16px;font-size:13.5px;line-height:1.45;color:#2A3450;margin-bottom:7px}
ul.l li:before{content:"";position:absolute;left:0;top:8px;width:8px;height:2px;background:#00AEEF}
.ask{position:absolute;left:0;right:0;bottom:0;background:#001F5B;color:#fff;padding:16px 22px;border-radius:6px;font-size:14px;line-height:1.45}
.ask b{color:#5FD0FA}
.navy{background:#001F5B;color:#fff}.navy p,.navy ul.l li{color:#D4DEEF}
.flag{display:inline-block;font-size:10.5px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;border-radius:3px}
.f-ok{background:#E3F6EC;color:#147A4A}.f-no{background:#FDECEC;color:#B42318}.f-mid{background:#FFF4DB;color:#8A5A00}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th{text-align:left;font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:#6B7690;padding:7px 10px;border-bottom:2px solid #001F5B}
td{padding:7px 10px;border-bottom:1px solid #E4E8F0;vertical-align:top;line-height:1.35}
td:first-child{font-weight:bold;color:#0A1226;width:150px}
td.new{color:#001F5B;font-weight:bold}
.shot{border:1px solid #E4E8F0;border-radius:6px;overflow:hidden;position:relative}
.shot img{display:block;width:100%;height:232px;object-fit:cover;object-position:top}
.shot span{position:absolute;left:8px;top:8px;background:rgba(0,31,91,.9);color:#fff;font-size:10px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;border-radius:3px}
.tl{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
.tl div{border-top:3px solid #00AEEF;padding-top:8px;font-size:12px;line-height:1.4;color:#3A4560}
.tl b{display:block;font-size:12.5px;color:#001F5B;margin-bottom:3px}
"""

def slide(n, sec, body, src):
    return ('<div class="s"><div class="hd"><img src="%s"><span>Website and brand &middot; %s</span></div><div class="bd">%s</div>'
            '<div class="ft"><span class="src">%s</span><span>Prolifics &middot; Internal &middot; November 2026 &middot; %d</span></div></div>' % (IMG("logo.png"), E(sec), body, src, n))

S = []

# 1. The four decisions
tiles = [
    ("Move off WordPress", "Retire the WordPress CMS and run a custom static site. A far smaller attack surface, faster pages, and content deployed by our team.", "No login page, database or plugins left for bots to probe."),
    ("prolifics.com is home", "Return to the 30 year old domain as the primary address. Keep prolifics.ai as the AI brand, redirected page by page.", "Thirty years of links and search history working for us again."),
    ("Launch the new site", "Replace today's home and practice pages with the new build, measured against the current site from day one.", "A site that shows 48 years of delivery and named results."),
    ("GCC Conclave in December", "10 to 15 GCC leaders on stage, enterprise CxOs in the room, Satya Bolli as a speaker. Second or third week of December.", "Prolifics in front of GCC leaders and their CxO peers."),
]
body = ('<p class="eb">Decisions for this week</p><h1>Four decisions to make prolifics.com secure, fast and ready for December</h1>'
        '<p class="sub">The website is our most visited sales asset. Today it runs on a platform we do not need, on a domain that is not our strongest, '
        'with content nobody is updating. These four moves fix that before we put 15 GCC leaders and a room of CxOs in front of the brand.</p>'
        '<div class="g" style="grid-template-columns:repeat(4,1fr);margin-top:26px">%s</div>'
        '<div class="ask"><b>What we need:</b> approval on all four this week, one marketing approver who signs off copy before it goes live, '
        'and a confirmed conclave date, city and venue.</div>') % "".join(
    '<div class="card" style="min-height:300px;display:flex;flex-direction:column"><span class="n">%d</span><h3 style="font-size:19px">%s</h3><p style="font-size:14px;flex:1">%s</p>'
    '<p style="border-top:1px solid #D9E2F0;padding-top:12px;margin-top:12px;color:#001F5B;font-weight:bold">%s</p></div>' % (i + 1, E(t), E(d), E(o)) for i, (t, d, o) in enumerate(tiles))
S.append(slide(1, "Summary", body, "Details and sources on the following pages."))

# 2. Off WordPress
stats = [("11,334", "", "new WordPress ecosystem vulnerabilities disclosed in 2025, up 42% on 2024. 91% were in plugins."),
         ("46", "%", "of those had no fix available when they were made public. Heavily targeted flaws were exploited in a median of 5 hours."),
         ("40", "%", "of all internet traffic in 2025 came from bad bots. Automated traffic overall was 53%.")]
body = ('<p class="eb">1. Platform</p><h1>WordPress is where the attacks land. We do not need it.</h1>'
        '<p class="sub">We are seeing bot traffic and attack attempts against prolifics.ai. The risk sits in the plugin ecosystem, and marketing no longer edits content in the CMS, '
        'so we carry the exposure without using the benefit.</p>'
        '<div class="g" style="grid-template-columns:1fr 1fr 1.05fr;margin-top:22px;gap:22px">'
        '<div><p class="k">The ecosystem risk</p>%s</div>'
        '<div class="card"><p class="k">What prolifics.ai exposes today</p><p style="font-size:11px;color:#6B7690;margin:-4px 0 10px">Checked with plain public requests, 19 Nov 2026</p><ul class="l">'
        '<li>WordPress with the Themify Ultra theme and 7 or more plugins loaded on the home page</li>'
        '<li>Public login page reachable at /wp-login.php</li><li>WordPress REST API open at /wp-json</li>'
        '<li>readme.html served, WordPress version visible in asset links</li><li>20 third party hosts and 44 script tags on the home page</li></ul></div>'
        '<div class="card navy"><p class="k" style="color:#5FD0FA">What we move to</p><ul class="l">'
        '<li>Custom static site served from a global CDN</li><li>No PHP, no database, no login page and no plugins on the public server</li>'
        '<li>Content written by us, reviewed, and deployed through version control. Nothing is lost: marketing is not editing in the CMS today</li>'
        '<li>New pages from templates in hours, not tickets</li><li>Forms and tracking stay in HubSpot and GA4</li></ul></div></div>') % "".join(
    '<div class="stat" style="margin-bottom:16px"><p class="big">%s<small>%s</small></p><p>%s</p></div>' % (n, u, E(d)) for n, u, d in stats)
S.append(slide(2, "Platform", body,
    "Sources: Patchstack, State of WordPress Security in 2026 (Feb 2026); Thales Bad Bot Report 2026 via Help Net Security (30 Apr 2026). "
    "Site checks: public HTTP requests to prolifics.ai on 19 Nov 2026."))

# 3. Domain
doms = [
    ("prolifics.com", "f-ok", "Make it home", "Registered 25 July 1996: 30 years of links, search history, email and client familiarity. "
     "Today it shows a holding page with a JavaScript redirect, and inner pages such as /services return 404, so old links break."),
    ("prolifics.ai", "f-mid", "Keep as the AI brand", "Registered 9 October 2025. A strong AI signal for campaigns and events, but a 13 month old domain with little search history."),
    ("prolifics.si", "f-no", "Not available", "Registered on 8 October 2026 by another party and parked. SI is the term US buyers use for firms like ours, but this name is taken."),
]
steps = [("Home", "Serve the new site on prolifics.com as the canonical address."),
         ("Redirect", "Every prolifics.ai page 301s to its prolifics.com match, server side, as Google recommends for site moves."),
         ("Brand", "prolifics.ai stays in AI campaigns, signatures and events, landing on the same pages."),
         ("Search", "File the change of address in Search Console and update HubSpot links and forms.")]
body = ('<p class="eb">2. Domain</p><h1>prolifics.com stays home. prolifics.ai carries the AI brand.</h1>'
        '<p class="sub">Thirty years of domain history is an asset no new name can buy. Done with proper redirects, we keep the AI signal of .ai and the trust of .com.</p>'
        '<div class="g" style="grid-template-columns:repeat(3,1fr);margin-top:22px">%s</div>'
        '<p class="k" style="margin-top:26px">The move, in four steps</p><div class="g" style="grid-template-columns:repeat(4,1fr)">%s</div>') % (
    "".join('<div class="card" style="min-height:206px"><p style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:21px;color:#001F5B">%s</b>'
            '<span class="flag %s">%s</span></p><p style="margin-top:12px">%s</p></div>' % (d, c, E(l), E(t)) for d, c, l, t in doms),
    "".join('<div style="border-top:3px solid #00AEEF;padding-top:10px"><span class="n" style="width:24px;height:24px;font-size:12px">%d</span>'
            '<b style="display:block;margin:8px 0 4px;color:#001F5B">%s</b><p style="font-size:12.5px;color:#3A4560;line-height:1.4">%s</p></div>' % (i + 1, E(h), E(t)) for i, (h, t) in enumerate(steps)))
S.append(slide(3, "Domain", body,
    "Sources: whois records for prolifics.com, prolifics.ai and prolifics.si; HTTP checks of www.prolifics.com, 19 Nov 2026; "
    "Google Search Central, Move a site with URL changes."))

# 4. New vs existing
rows = [("Message", "Generic AI expertise claims", "48 years of making enterprise technology work, now AI in production"),
        ("Platform", "WordPress, Themify Ultra theme, plugins", "Custom static build on a CDN"),
        ("Third party hosts", "20", "2"),
        ("Script tags", "44", "1, inline"),
        ("Page load, same test", "2.4 s", "1.5 s"),
        ("Proof on the page", "Headline numbers only", "9 published case studies with results"),
        ("Content updates", "Depend on CMS edits that are not happening", "Deployed by our team every week")]
body = ('<p class="eb">3. The site</p><h1>New site vs existing: the aim, and where we are</h1>'
        '<p class="sub"><b>Aim:</b> be found, believed and booked by enterprise buyers and by AI search. Baseline today is about 5,800 sessions a month in HubSpot; the goal is to double it.</p>'
        '<div class="g" style="grid-template-columns:420px 1fr;gap:26px;margin-top:16px"><div class="g" style="gap:10px">'
        '<div class="shot"><span>Existing, prolifics.ai</span><img src="%s"></div><div class="shot"><span>New home page</span><img src="%s"></div></div>'
        '<div><table><tr><th></th><th>Existing</th><th>New</th></tr>%s</table>'
        '<div class="g" style="grid-template-columns:1fr 1fr;margin-top:14px;gap:12px"><div class="card" style="padding:12px 16px"><p class="k" style="margin-bottom:6px">Done</p>'
        '<p>New home page in two designs; 85 practice pages for Salesforce, ServiceNow and FDE on preview.</p></div>'
        '<div class="card" style="padding:12px 16px"><p class="k" style="margin-bottom:6px">Next</p><p>Inner pages, URL map and redirects, HubSpot forms and GA4, launch on prolifics.com before the conclave.</p></div></div></div></div>') % (
    IMG("old_hero.png"), IMG("new_hero.png"), "".join('<tr><td>%s</td><td>%s</td><td class="new">%s</td></tr>' % (E(a), E(b), E(c)) for a, b, c in rows))
S.append(slide(4, "New site", body,
    "Measured on 19 Nov 2026 in the same desktop browser, home page only (load event). Mobile PageSpeed scores to follow: the public API was rate limited. "
    "Sessions: HubSpot, November 2026."))

# 5. GCC Conclave
tl = [("This week", "Confirm date, city, venue and the invite list"), ("Next week", "Speaker confirmations; event page on prolifics.com"),
      ("Weeks 3 to 4", "Invitations, follow ups, briefing pack for speakers"), ("Event", "Second or third week of December"),
      ("After", "Recordings and insights on the site; follow up meetings")]
body = ('<div class="g" style="grid-template-columns:1fr 430px;gap:36px;height:100%%"><div><p class="eb">4. GCC Conclave</p>'
        '<h1>The Prolifics GCC Conclave, December 2026</h1><p class="sub">An invitation only gathering where global capability center leaders share how they are building AI ready teams, '
        'in front of CxOs from large enterprises. Satya Bolli speaks.</p>'
        '<div class="g" style="grid-template-columns:repeat(3,1fr);margin-top:20px">'
        '<div class="stat"><p class="big">2,117</p><p>GCCs in India in FY26</p></div><div class="stat"><p class="big">2.36<small>M</small></p><p>people working in them</p></div>'
        '<div class="stat"><p class="big">$98.4<small>B</small></p><p>revenue, FY26</p></div></div>'
        '<div class="g" style="grid-template-columns:1fr 1fr;margin-top:20px;gap:14px"><div class="card"><p class="k">Format</p><ul class="l">'
        '<li>10 to 15 GCC leaders as speakers</li><li>CxOs from large enterprises as the audience</li><li>Satya Bolli on stage</li><li>City and venue to confirm</li></ul></div>'
        '<div class="card"><p class="k">Proposed run of show</p><ul class="l"><li>Opening: Satya Bolli on 48 years and what AI ready means</li>'
        '<li>Panel: GCCs as capability centers, not cost centers</li><li>Panel: getting AI agents into production</li><li>Closing roundtable and dinner</li></ul></div></div>'
        '<p class="k" style="margin-top:18px">Timeline</p><div class="tl">%s</div></div>'
        '<div style="position:relative;border-radius:8px;overflow:hidden;background:#001F5B"><img src="%s" style="width:100%%;height:100%%;object-fit:cover;opacity:.55">'
        '<img src="%s" style="position:absolute;right:-10px;bottom:0;height:78%%">'
        '<div style="position:absolute;left:22px;top:22px;right:22px;color:#fff"><p style="font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:bold;color:#5FD0FA">Speaker</p>'
        '<p style="font-size:22px;font-weight:bold;margin-top:6px">Satya Bolli</p><p style="font-size:13px;color:#D4DEEF">Chairman and Managing Director, Prolifics</p></div></div></div>') % (
    "".join('<div><b>%s</b>%s</div>' % (E(a), E(b)) for a, b in tl), IMG("conf.jpg"), IMG("satya.png"))
S.append(slide(5, "GCC Conclave", body, "Source: Nasscom and Zinnov, India GCC landscape, press release (6 May 2026). Event format, run of show and timeline are proposals for approval."))

doc = '<!doctype html><html><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>' % (E(NAME), CSS, "".join(S))
h = os.path.join(OUT, NAME + ".html"); open(h, "w", encoding="utf-8").write(doc)
pdf = os.path.join(OUT, NAME + ".pdf")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=6000", "--print-to-pdf=" + pdf, "file://" + h], capture_output=True, timeout=180)
txt = re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>", "", doc, flags=re.S))
print("pdf", os.path.exists(pdf), "dashes", len(re.findall("[–—]", txt)), "excl", txt.count("!"))
