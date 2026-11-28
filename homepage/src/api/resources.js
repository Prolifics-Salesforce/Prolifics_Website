// Vercel serverless function: the Resource Center library, read live from the corporate site (prolifics.ai, WordPress).
//   GET /api/resources                      -> { items, total, pages, page, types }   newest first, 12 per page
//   GET /api/resources?type=blog&q=ai&page=2   filter by type (category slug), search, and page through
//   GET /api/resources?slug=<slug>          -> { item: {...} }   one article with its body, or 404
// Blogs, case studies, news, briefs and one pagers published on prolifics.ai show here with no change to this site.
// Answers are cached for about five minutes. If prolifics.ai cannot be reached, the last good copy is served.
//
// Environment variable (optional): RESOURCES_SOURCE, the site to read from. Default https://prolifics.ai
// Article bodies are HTML written in WordPress. They are cleaned here: simple formatting, links, images and tables
// only, so no script, style, frame or event handler can reach the page.

const SITE = (process.env.RESOURCES_SOURCE || "https://prolifics.ai").replace(/\/+$/, "");
const API = SITE + "/wp-json/wp/v2";
const PER_PAGE = 12, TTL = 5 * 60 * 1000, MAX_CACHE = 300;
const ORDER = ["blog", "case-studies", "news", "briefs", "one-pager", "industry"];   // filter order; other types follow
const LABEL = { blog: "Blogs", "one-pager": "One Pagers" };                         // plural where WordPress has the singular
const SLUG = /^[a-z0-9][a-z0-9-]{0,199}$/;
const cache = new Map();

async function wp(path) {
  const hit = cache.get(path), now = Date.now();
  if (hit && now - hit.at < TTL) return hit.val;
  try {
    const r = await fetch(API + path, { headers: { Accept: "application/json", "User-Agent": "Mozilla/5.0 (compatible; ProlificsWebsite/1.0)" }, signal: AbortSignal.timeout(9000) });
    if (!r.ok) throw new Error("status " + r.status);
    const val = { data: await r.json(), total: Number(r.headers.get("x-wp-total")) || 0, pages: Number(r.headers.get("x-wp-totalpages")) || 0 };
    if (cache.size >= MAX_CACHE) cache.delete(cache.keys().next().value);
    cache.set(path, { at: now, val });
    return val;
  } catch (e) {
    if (hit) return hit.val;   // keep showing the last good copy
    throw e;
  }
}

const NAMED = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", hellip: "...", rsquo: "\u2019", lsquo: "\u2018", rdquo: "\u201D", ldquo: "\u201C", ndash: "\u2013", mdash: "\u2014" };
function decode(s) {
  return String(s || "").replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] !== "#") return NAMED[e.toLowerCase()] != null ? NAMED[e.toLowerCase()] : m;
    const n = e[1].toLowerCase() === "x" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
    return n > 0 && n < 0x110000 ? String.fromCodePoint(n) : "";
  });
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const text = (html) => decode(String(html || "").replace(/<[^>]+>/g, " ")).replace(/\s+/g, " ").trim();
function excerpt(html) {
  const t = text(html).replace(/\s*(\[\u2026\]|\[\.\.\.\]|\u2026)\s*$/, "");
  if (t.length <= 190) return t;
  return t.slice(0, 190).replace(/\s+\S*$/, "") + "...";
}
function attr(attrs, name) {
  const m = attrs.match(new RegExp("\\b" + name + "\\s*=\\s*(?:\"([^\"]*)\"|'([^']*)'|([^\\s>]+))", "i"));
  return m ? decode(m[1] || m[2] || m[3] || "").trim() : "";
}
// A link to another library item on the corporate site opens that item on this site instead.
function localLink(url) {
  const m = url.match(/^https?:\/\/(?:www\.)?prolifics\.ai\/resource-center\/[a-z0-9-]+\/([a-z0-9-]+)\/?(?:[?#].*)?$/i);
  return m ? "/resources/article/" + m[1].toLowerCase() : url;
}

const TAGS = new Set(["p", "br", "strong", "b", "em", "i", "u", "ul", "ol", "li", "h2", "h3", "h4", "blockquote", "a", "img", "figure", "figcaption",
                      "table", "thead", "tbody", "tr", "th", "td"]);
function cleanBody(html) {
  let s = String(html || "").replace(/<!--[\s\S]*?-->/g, "").replace(/<(script|style|iframe|object|embed|template|svg|math|form|noscript)\b[\s\S]*?<\/\1\s*>/gi, "");
  s = s.replace(/<\/?([a-z][a-z0-9]*)\b([^>]*)>/gi, (m, name, attrs) => {
    const tag = name.toLowerCase(), closing = m[1] === "/";
    if (tag === "h1") return closing ? "</h2>" : "<h2>";
    if (tag === "h5" || tag === "h6") return closing ? "</h4>" : "<h4>";
    if (!TAGS.has(tag)) return "";   // the tag goes, its text stays
    if (closing) return tag === "img" || tag === "br" ? "" : "</" + tag + ">";
    if (tag === "a") {
      const url = localLink(attr(attrs, "href"));
      return /^(https?:\/\/|mailto:|\/(?!\/))/i.test(url) ? '<a href="' + esc(url) + '" rel="noopener">' : "<a>";
    }
    if (tag === "img") {
      const src = attr(attrs, "src");
      return /^https:\/\//i.test(src) ? '<img src="' + esc(src) + '" alt="' + esc(attr(attrs, "alt")) + '" loading="lazy">' : "";
    }
    return "<" + tag + ">";
  });
  return s.replace(/<(?![/a-z])/gi, "&lt;").replace(/<p>\s*<\/p>/g, "").replace(/\n{3,}/g, "\n\n").trim();
}

async function types() {
  const cats = (await wp("/categories?per_page=100&_fields=id,slug,name,count")).data;
  const list = cats.filter((c) => c.count > 0 && c.slug !== "uncategorized").map((c) => ({ id: c.id, slug: c.slug, label: LABEL[c.slug] || decode(c.name), count: c.count }));
  const rank = (t) => { const i = ORDER.indexOf(t.slug); return i < 0 ? ORDER.length : i; };
  return list.sort((a, b) => rank(a) - rank(b) || a.label.localeCompare(b.label));
}

function image(p) {
  const m = p._embedded && p._embedded["wp:featuredmedia"] && p._embedded["wp:featuredmedia"][0];
  if (!m || !m.source_url) return null;
  const sizes = (m.media_details && m.media_details.sizes) || {}, pick = sizes.medium_large || sizes.large || sizes.full;
  const ok = (u) => /^https:\/\//i.test(u || "");
  if (!ok(m.source_url)) return null;
  return { url: m.source_url, thumb: pick && ok(pick.source_url) ? pick.source_url : m.source_url, alt: text(m.alt_text) };
}
function view(p, all, full) {
  const t = all.find((c) => (p.categories || []).includes(c.id));
  const o = { slug: p.slug, title: text(p.title && p.title.rendered), date: String(p.date || "").slice(0, 10),
              type: t ? { slug: t.slug, label: decode(t.label) } : null, excerpt: excerpt(p.excerpt && p.excerpt.rendered), image: image(p) };
  if (full) o.body = cleanBody(p.content && p.content.rendered);
  return o;
}

module.exports = async function handler(req, res) {
  const send = (code, obj, cacheable) => {
    res.statusCode = code;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", cacheable ? "public, s-maxage=300, stale-while-revalidate=3600" : "no-store");
    res.end(JSON.stringify(obj));
  };
  if (req.method !== "GET" && req.method !== "HEAD") { res.setHeader("Allow", "GET"); return send(405, { error: "Method not allowed" }); }
  const q = new URL(req.url, "http://localhost").searchParams;
  try {
    const all = await types();
    const slug = q.get("slug");
    if (slug != null) {
      if (!SLUG.test(slug)) return send(404, { error: "Not found" });
      const p = (await wp("/posts?slug=" + slug + "&_embed=wp:featuredmedia")).data[0];
      return p ? send(200, { item: view(p, all, true) }, true) : send(404, { error: "Not found" });
    }
    const type = all.find((c) => c.slug === q.get("type")), search = (q.get("q") || "").trim().slice(0, 80);
    const page = Math.min(Math.max(parseInt(q.get("page"), 10) || 1, 1), 500);
    let path = "/posts?per_page=" + PER_PAGE + "&page=" + page + "&_embed=wp:featuredmedia&_fields=slug,date,title,excerpt,categories,_links,_embedded";
    if (type) path += "&categories=" + type.id;
    if (search) path += "&search=" + encodeURIComponent(search);
    let r;
    try { r = await wp(path); }
    catch (e) { if (page > 1 && /status 400/.test(e.message)) r = { data: [], total: 0, pages: page - 1 }; else throw e; }   // past the last page
    return send(200, { items: r.data.map((p) => view(p, all, false)), total: r.total, pages: r.pages, page,
                       types: all.map((c) => ({ slug: c.slug, label: c.label })) }, true);
  } catch (e) {
    console.error("Resources could not be read: " + e.message);
    return send(502, { error: "Resources are not available right now" });
  }
};
