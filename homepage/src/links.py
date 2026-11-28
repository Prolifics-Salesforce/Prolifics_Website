"""Outside links (28 Nov 2026): nothing on this site links to prolifics.ai, casestudies.com, prolifics-testing.com or
YouTube. Both builders pass every page through delink() before writing it, then check() stops the build if a link to
prolifics.ai is still there.

delink() works on the finished HTML, so it covers every place a link can come from (content.py, cases.py,
pages_content.py, ref.json):
  - a prolifics.ai case study that is published in the HubSpot blog opens as an article on this site; any other case
    study link (prolifics.ai, casestudies.com, prolifics-testing.com) goes to the case study library on this site
  - a prolifics.ai page with a twin here (about, locations, contact, the legal pages, ...) goes to that page
  - the old hard-coded planning guide pages go to the same guide in the HubSpot library, or to the planning guide library
  - a YouTube link goes to the video library
  - anything else on those hosts loses its link and keeps its text

The list of published article slugs is read from HubSpot once per build, with the same HUBSPOT_ACCESS_TOKEN the site
uses (from the environment, or from .env.local next to dev_server.js). If HubSpot cannot be reached the build still
works: case study links then all go to the case study library.
"""
import os, re, json, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CASE_LIB, GUIDE_LIB, VIDEO_LIB = "/resources?type=case-study#library", "/resources?type=planning-guide#library", "/resources?type=video#library"
OLD_GUIDES = ("/resources/forward-deployed-ai-vs-consulting", "/resources/ai-data-readiness", "/resources/enterprise-ai-evaluation")
PAGES = {"": "/", "about-us": "/about", "leadership": "/about/leadership", "locations": "/about/locations", "careers": "/about/careers",
         "contact": "/contact", "partnerships": "/partnerships", "resource-center": "/resources", "events": "/events",
         "privacy-policy": "/privacy-policy", "cookie-policy": "/cookie-policy", "legal-notice": "/legal-notice",
         "resource-center/case-studies": CASE_LIB, "resource-center/blogs": "/resources?type=blog#library", "resource-center/news": "/resources?type=news#library",
         "resource-center/one-pagers": "/resources?type=one-pager#library"}
BANNED = re.compile(r"^https?://(?:[^/]*\.)?(prolifics\.ai|casestudies\.com|prolifics-testing\.com|youtube\.com|youtu\.be)(?:[/?#]|$)", re.I)
_slugs = None

def _token():
    t = os.environ.get("HUBSPOT_ACCESS_TOKEN") or os.environ.get("HUBSPOT_TOKEN")
    if t: return t
    try:
        for line in open(os.path.join(HERE, "..", ".env.local"), encoding="utf-8"):
            m = re.match(r"\s*HUBSPOT_(?:ACCESS_)?TOKEN\s*=\s*(.+?)\s*$", line)
            if m: return m.group(1).strip("\"'")
    except OSError:
        pass
    return ""

def hubspot_slugs():
    """Slugs of the published posts in the HubSpot blog "Resources" (an empty set if HubSpot cannot be read)."""
    global _slugs
    if _slugs is not None: return _slugs
    _slugs, token, after = set(), _token(), ""
    if not token:
        print("  links: no HubSpot token, case study links all go to the case study library"); return _slugs
    try:
        for _ in range(50):
            url = ("https://api.hubapi.com/cms/v3/blogs/posts?contentGroupId=%s&state=PUBLISHED&limit=100" % os.environ.get("HUBSPOT_BLOG_ID", "228825805709")
                   + ("&after=" + after if after else ""))
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
            j = json.load(urllib.request.urlopen(req, timeout=20))
            for p in j.get("results", []):
                _slugs.add(str(p.get("slug", "")).lower().rstrip("/").split("/")[-1])
            after = ((j.get("paging") or {}).get("next") or {}).get("after") or ""
            if not after: break
    except Exception as e:   # the build must not depend on HubSpot being up
        print("  links: HubSpot could not be read (%s), case study links all go to the case study library" % type(e).__name__)
    return _slugs

def target(url):
    """The on-site address for an outside link, "" to drop the link and keep its text, or None to leave it alone."""
    if url in OLD_GUIDES:   # the same guide in HubSpot if it is published there, otherwise the guide library
        s = url.split("/")[-1]
        return "/resources/article/" + s if s in hubspot_slugs() else GUIDE_LIB
    m = BANNED.match(url)
    if not m: return None
    host, path = m.group(1).lower(), re.sub(r"^https?://[^/]+/?", "", url).split("#")[0].split("?")[0].strip("/").lower()
    if host in ("youtube.com", "youtu.be"): return VIDEO_LIB
    if host == "casestudies.com": return CASE_LIB
    if host == "prolifics-testing.com": return CASE_LIB if path.startswith("case-studies/") else ""
    lib = re.match(r"resource-center/([a-z0-9-]+)/([a-z0-9_-]+)$", path)
    if lib:
        if lib.group(2) in hubspot_slugs(): return "/resources/article/" + lib.group(2)
        return CASE_LIB if lib.group(1) == "case-studies" else "/resources"
    if path in PAGES: return PAGES[path]
    return "/partnerships" if path.startswith("partnerships/") else ""

def delink(html):
    def rep(m):
        attrs, inner = m.group(1), m.group(2)
        h = re.search(r'\bhref="([^"]*)"', attrs)
        if not h: return m.group(0)
        to = target(h.group(1).replace("&amp;", "&"))
        if to is None: return m.group(0)
        rest = re.sub(r'\s+(?:href|rel|target)="[^"]*"', "", attrs)
        if to == "": return "<span%s>%s</span>" % (rest, inner)
        return '<a%s href="%s">%s</a>' % (rest, to, inner)
    return re.sub(r"<a\b([^>]*)>(.*?)</a>", rep, html, flags=re.S)

def check(html, name):
    """Stops the build if a page still links to, or loads anything from, prolifics.ai."""
    bad = sorted(set(re.findall(r'\b(?:href|src|srcset|action|poster|data-src)="([^"]*prolifics\.ai[^"]*)"', html, flags=re.I)))
    if bad:
        sys.exit("BUILD STOPPED: %s still links to prolifics.ai: %s" % (name, ", ".join(bad[:5])))
