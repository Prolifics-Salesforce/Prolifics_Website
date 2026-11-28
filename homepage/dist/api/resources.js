// Vercel serverless function: the Resources library, read from HubSpot (blog "Resources" and HubDB table resource_items).
//   GET /api/resources                          -> { items, total, pages, page, types }   12 per page, in display order
//   GET /api/resources?type=blog&q=ai&page=2    filter by type, search titles and summaries, page through
//   GET /api/resources?slug=<slug>              -> { item: {...} }   one item with its body, or 404
// Types: blog, news, case-study, planning-guide (blog posts) and one-pager, video (table rows).
// Marketing publishes in HubSpot and the site follows within about a minute; nothing here needs rebuilding.
// Everything opens on this site: posts at /resources/article/<slug>, table rows at /resources/item/<slug>.
// The reading, caching and token handling are in _resources.js. The browser never sees the token or talks to HubSpot.
//
// Article and row bodies are HTML written in HubSpot. They are cleaned here: simple formatting, links, images and
// tables only, so no script, style, frame or event handler can reach the page.
const store = require("./_resources.js");

const PER_PAGE = 12;
const ALIAS = { "case-studies": "case-study", "one-pagers": "one-pager", blogs: "blog", videos: "video", "planning-guides": "planning-guide" };
const SLUG = /^[a-z0-9][a-z0-9_-]{0,199}$/;

// Links in article text that point at the old corporate site (prolifics.ai) never leave this site: a library item
// opens here if it is in the library, a known page goes to its page here, and anything else loses the link but keeps
// its text. Images hosted there are dropped.
const OLD = /^https?:\/\/(?:www\.)?prolifics\.ai(?:\/([^?#]*))?(?:[?#].*)?$/i;
const PAGES = { "": "/", contact: "/contact", "about-us": "/about", leadership: "/about/leadership", locations: "/about/locations", careers: "/about/careers",
  partnerships: "/partnerships", "resource-center": "/resources", events: "/events", "ai-services": "/services/ai-services", "data-ai": "/services/data-ai",
  "data-ai-governance": "/services/data-governance", "ai-maturity-readiness": "/services/ai-maturity", "data-engineering": "/services/data-engineering",
  "testing-for-ai": "/services/testing-for-ai", mlops: "/services/mlops", "data-assessment": "/services/data-assessment",
  "ai-powered-expertise/generative-ai": "/services/generative-ai", "ai-as-a-service-aiaas": "/services/aiaas", salesforce: "/services/salesforce",
  sap: "/services/sap", "privacy-policy": "/privacy-policy", "cookie-policy": "/cookie-policy", "legal-notice": "/legal-notice" };
function onSite(url, known) {
  const m = url.match(OLD);
  if (!m) return url;
  const path = (m[1] || "").replace(/\/+$/, "").toLowerCase(), lib = path.match(/^resource-center\/[a-z0-9-]+\/([a-z0-9_-]+)$/);
  if (lib) return known.has(lib[1]) ? "/resources/article/" + lib[1] : "";
  if (PAGES[path] != null) return PAGES[path];
  return /^partnerships\//.test(path) ? "/partnerships" : "";
}

const NAMED = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " " };
function decode(s) {
  return String(s || "").replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] !== "#") return NAMED[e.toLowerCase()] != null ? NAMED[e.toLowerCase()] : m;
    const n = e[1].toLowerCase() === "x" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
    return n > 0 && n < 0x110000 ? String.fromCodePoint(n) : "";
  });
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function attr(attrs, name) {
  const m = attrs.match(new RegExp("\\b" + name + "\\s*=\\s*(?:\"([^\"]*)\"|'([^']*)'|([^\\s>]+))", "i"));
  return m ? decode(m[1] || m[2] || m[3] || "").trim() : "";
}
function short(s) {
  const t = String(s || "").replace(/\s+/g, " ").trim();
  return t.length <= 190 ? t : t.slice(0, 190).replace(/\s+\S*$/, "") + "...";
}

const TAGS = new Set(["p", "br", "strong", "b", "em", "i", "u", "ul", "ol", "li", "h2", "h3", "h4", "blockquote", "a", "img", "figure", "figcaption",
                      "table", "thead", "tbody", "tr", "th", "td"]);
// "known" holds the slugs of the articles in the library.
function cleanBody(html, known) {
  let s = String(html || "").trim();
  if (!s) return "";
  if (!/<[a-z][\s\S]*>/i.test(s)) return s.split(/\n\s*\n/).map((p) => "<p>" + esc(p.trim()).replace(/\n/g, "<br>") + "</p>").join("");
  s = s.replace(/<!--[\s\S]*?-->/g, "").replace(/<(script|style|iframe|object|embed|template|svg|math|form|noscript)\b[\s\S]*?<\/\1\s*>/gi, "");
  s = s.replace(/<\/?([a-z][a-z0-9]*)\b([^>]*)>/gi, (m, name, attrs) => {
    const tag = name.toLowerCase(), closing = m[1] === "/";
    if (tag === "h1") return closing ? "</h2>" : "<h2>";
    if (tag === "h5" || tag === "h6") return closing ? "</h4>" : "<h4>";
    if (!TAGS.has(tag)) return "";   // the tag goes, its text stays
    if (closing) return tag === "img" || tag === "br" ? "" : "</" + tag + ">";
    if (tag === "a") {
      const url = onSite(attr(attrs, "href"), known);
      return /^(https?:\/\/|mailto:|\/(?!\/))/i.test(url) ? '<a href="' + esc(url) + '"' + (url[0] === "/" ? "" : ' rel="noopener"') + ">" : "<a>";
    }
    if (tag === "img") {
      const src = attr(attrs, "src");
      return /^https:\/\//i.test(src) && !OLD.test(src) ? '<img src="' + esc(src) + '" alt="' + esc(attr(attrs, "alt")) + '" loading="lazy">' : "";
    }
    return "<" + tag + ">";
  });
  s = s.replace(/<a>([\s\S]*?)<\/a>/g, "$1");   // a link that was removed keeps its text
  return s.replace(/<(?![/a-z])/gi, "&lt;").replace(/<p>\s*<\/p>/g, "").replace(/\n{3,}/g, "\n\n").trim();
}

// What the browser gets. "path" is where a card leads: always a page on this site.
function view(x, full) {
  const o = { slug: x.slug, title: x.title, date: x.date, type: x.type, excerpt: short(x.summary), image: x.image, featured: x.featured,
              path: (x.kind === "post" ? "/resources/article/" : "/resources/item/") + x.slug, video: x.video || null };
  if (full && x.kind === "row") { o.summary = x.summary; o.file = x.file || null; }   // the file is offered as a download, on the item page only
  return o;
}

module.exports = async function handler(req, res) {
  const send = (code, obj, cacheable) => {
    res.statusCode = code;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", cacheable ? "public, s-maxage=30" : "no-store");
    res.end(JSON.stringify(obj));
  };
  if (req.method !== "GET" && req.method !== "HEAD") { res.setHeader("Allow", "GET"); return send(405, { error: "Method not allowed" }); }
  const q = new URL(req.url, "http://localhost").searchParams;
  try {
    const all = await store.items();
    const slug = q.get("slug");
    if (slug != null) {
      const x = SLUG.test(slug) ? all.find((y) => y.slug === slug) : null;
      if (!x) return send(404, { error: "Not found" });
      const item = view(x, true), known = new Set(all.filter((y) => y.kind === "post").map((y) => y.slug));
      item.body = cleanBody(x.kind === "post" ? await store.postBody(x) : x.body, known);
      return send(200, { item }, true);
    }
    const want = (q.get("type") || "").toLowerCase(), type = ALIAS[want] || want, search = (q.get("q") || "").trim().slice(0, 80).toLowerCase();
    const page = Math.min(Math.max(parseInt(q.get("page"), 10) || 1, 1), 500);
    let list = all;
    if (type) list = list.filter((x) => x.type.slug === type);
    if (search) { const words = search.split(/\s+/); list = list.filter((x) => { const hay = (x.title + " " + x.summary).toLowerCase(); return words.every((w) => hay.includes(w)); }); }
    const types = store.TYPES.filter((t) => all.some((x) => x.type.slug === t.slug)).map((t) => ({ slug: t.slug, label: t.label }));   // only types that have something
    return send(200, { items: list.slice((page - 1) * PER_PAGE, page * PER_PAGE).map((x) => view(x, false)), total: list.length,
                       pages: Math.max(1, Math.ceil(list.length / PER_PAGE)), page, type: type || "", types }, true);
  } catch (e) {
    console.error("Resources could not be read: " + e.message);
    return send(502, { error: "Resources are not available right now" });
  }
};
