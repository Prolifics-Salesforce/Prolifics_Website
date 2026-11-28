// Shared reader for the Resources section. The leading underscore keeps Vercel from exposing this file as a route;
// resources.js requires it. Same pattern as _hubdb.js (Events): read on the server with HUBSPOT_ACCESS_TOKEN, cache in
// memory, serve the last good copy if HubSpot cannot be reached. The token never leaves the server.
//
// Two HubSpot sources become one list:
//   1. Blog "Resources" (articles). Published posts only, every page of them. Each post carries one of four tags,
//      matched by tag NAME, which is its type: Blog, News, Case Study, Planning Guide. The slug plays no part in the
//      type. Posts with none of the four tags are left out.
//   2. HubDB table resource_items (short listings): One Pager (link is a file to download) and Video (link is a
//      YouTube address, played in an embedded player). Rows with status "published" only. A visitor is never sent
//      to the link itself.
// Order: featured rows first, then newest first.
//
// Environment variables:
//   HUBSPOT_ACCESS_TOKEN    required (the same key the lead form and Events use; scopes content, hubdb.rows.read)
//   HUBSPOT_BLOG_ID         blog (content group) ID, default 228825805709
//   HUBDB_RESOURCES_TABLE   table name or ID, default "resource_items"

const API = "https://api.hubapi.com";
const TTL = 30 * 1000;   // with the 30 second page cache in resources.js, an edit in HubSpot shows within a minute
const TYPES = [   // filter order on the page; "tag" is the blog tag name, "option" the HubDB select option
  { slug: "blog", label: "Blogs", tag: "blog" }, { slug: "news", label: "News", tag: "news" },
  { slug: "case-study", label: "Case Studies", tag: "case study" }, { slug: "planning-guide", label: "Planning Guides", tag: "planning guide" },
  { slug: "one-pager", label: "One Pagers", option: "one_pager" }, { slug: "video", label: "Videos", option: "video" },
];
const SLUG = /^[a-z0-9][a-z0-9_-]{0,199}$/;   // HubSpot keeps an underscore from the title in the slug
const OLD_SITE = /^https?:\/\/([^/]*\.)?prolifics\.ai(\/|$)/i;   // nothing is loaded from, or linked to, the old corporate site
const YOUTUBE = /^https:\/\/([^/]*\.)?(youtube\.com|youtube-nocookie\.com|youtu\.be)(\/|$)/i;
let cache = { at: 0, items: null };
const bodies = new Map();   // post id -> { at, html }

const text = (v) => (v == null ? "" : String(v).trim());
const https = (u) => (/^https:\/\//i.test(text(u)) && !OLD_SITE.test(text(u)) ? text(u) : "");
const day = (ms) => (ms == null || !isFinite(ms) ? "" : new Date(ms).toISOString().slice(0, 10));
const stamp = (v) => (typeof v === "number" && isFinite(v) ? v : (v && !isNaN(Date.parse(v)) ? Date.parse(v) : null));
const opt = (x) => text(x && typeof x === "object" ? (x.name || x.label) : x).toLowerCase().replace(/[\s-]+/g, "_");   // select values arrive as objects

async function hs(path) {
  const token = process.env.HUBSPOT_ACCESS_TOKEN || process.env.HUBSPOT_TOKEN;
  if (!token) throw new Error("HUBSPOT_ACCESS_TOKEN is not set");
  const r = await fetch(API + path, { headers: { Authorization: "Bearer " + token }, signal: AbortSignal.timeout(9000) });
  if (!r.ok) throw new Error("status " + r.status + " for " + path.split("?")[0]);
  return r.json();
}
// Every page of a HubSpot list: follows the "after" cursor until there is none.
async function pages(path, max) {
  const out = [];
  let after = "";
  for (let i = 0; i < max; i++) {
    const j = await hs(path + (after ? "&after=" + encodeURIComponent(after) : ""));
    (j.results || []).forEach((x) => out.push(x));
    after = j.paging && j.paging.next && j.paging.next.after;
    if (!after) break;
  }
  return out;
}

function youtubeId(url) {
  const m = text(url).match(/(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/|v\/))([A-Za-z0-9_-]{11})/i);
  return m ? m[1] : "";
}

async function posts() {
  const blog = encodeURIComponent(process.env.HUBSPOT_BLOG_ID || "228825805709");
  const tags = await pages("/cms/v3/blogs/tags?limit=100", 10), byTag = {};
  tags.forEach((t) => { const type = TYPES.find((x) => x.tag === text(t.name).toLowerCase()); if (type) byTag[String(t.id)] = type; });
  const list = await pages("/cms/v3/blogs/posts?contentGroupId=" + blog + "&state=PUBLISHED&sort=-publishDate&limit=100", 50), now = Date.now();
  return list.map((p) => {
    const type = (p.tagIds || []).map((id) => byTag[String(id)]).find(Boolean), when = stamp(p.publishDate), img = https(p.featuredImage);
    const slug = text(p.slug).toLowerCase().replace(/\/+$/, "").split("/").pop();   // HubSpot gives "resources/<folders>/<slug>"
    if (!type || !text(p.name) || !SLUG.test(slug) || p.state !== "PUBLISHED" || (when != null && when > now)) return null;   // drafts, scheduled, untagged
    if (typeof p.postBody === "string") bodies.set(String(p.id), { at: now, html: p.postBody });
    return { kind: "post", id: String(p.id), slug, title: text(p.name), type: { slug: type.slug, label: type.label }, summary: text(p.metaDescription),
             date: day(when), at: when || 0, featured: false, image: img ? { url: img, thumb: img, alt: text(p.featuredImageAltText) } : null };
  }).filter(Boolean);
}

async function rows() {
  const table = encodeURIComponent(process.env.HUBDB_RESOURCES_TABLE || "resource_items");
  const list = await pages("/cms/v3/hubdb/tables/" + table + "/rows?limit=200", 25);
  return list.map((row) => {
    const v = row.values || {}, type = TYPES.find((x) => x.option && x.option === opt(v.type)), slug = text(v.slug).toLowerCase();
    if (!type || !text(v.name) || !SLUG.test(slug) || opt(v.status) !== "published") return null;
    const when = stamp(v.publish_date), link = https(v.link), video = youtubeId(link);
    const file = link && !video && !YOUTUBE.test(link) ? link : "";   // a file to download, never a page to visit
    let img = v.image && typeof v.image === "object" ? https(v.image.url) : "", alt = img ? text(v.image.altText) : "";
    if (!img && video) img = "https://i.ytimg.com/vi/" + video + "/hqdefault.jpg";   // a video with no picture uses its YouTube thumbnail
    return { kind: "row", slug, title: text(v.name), type: { slug: type.slug, label: type.label }, summary: text(v.summary), date: day(when), at: when || 0,
             featured: v.featured === 1 || v.featured === true, image: img ? { url: img, thumb: img, alt } : null, file, video, body: text(v.body) };
  }).filter(Boolean);
}

async function load() {
  const [a, b] = await Promise.allSettled([posts(), rows()]);
  if (a.status === "rejected" && b.status === "rejected") throw new Error(a.reason.message + "; " + b.reason.message);
  if (a.status === "rejected") console.error("Resources: blog posts could not be read. " + a.reason.message);
  if (b.status === "rejected") console.error("Resources: table rows could not be read. " + b.reason.message);
  const seen = new Set(), all = [];
  (a.value || []).concat(b.value || []).forEach((x) => { if (!seen.has(x.slug)) { seen.add(x.slug); all.push(x); } });   // a post wins a slug clash
  return { items: all.sort((x, y) => (x.featured !== y.featured ? (x.featured ? -1 : 1) : y.at - x.at)), partial: a.status === "rejected" || b.status === "rejected" };
}

// Every visible item, in display order. If HubSpot is unreachable, the last good copy is served.
async function items() {
  if (cache.items && Date.now() - cache.at < TTL) return cache.items;
  try {
    const r = await load();
    if (r.partial && cache.items) { cache.at = Date.now(); console.error("Resources: serving the last good copy."); }
    else cache = { at: Date.now(), items: r.items };
  } catch (e) {
    if (!cache.items) throw e;
    cache.at = Date.now();
    console.error("Resources: serving the last good copy. " + e.message);
  }
  return cache.items;
}

async function find(slug) {
  const s = text(slug).toLowerCase();
  return (await items()).find((x) => x.slug === s) || null;
}

// The article HTML of a blog post, as written in HubSpot (not yet cleaned).
async function postBody(item) {
  const hit = bodies.get(item.id);
  if (hit && Date.now() - hit.at < TTL) return hit.html;
  try {
    const p = await hs("/cms/v3/blogs/posts/" + encodeURIComponent(item.id));
    bodies.set(item.id, { at: Date.now(), html: text(p.postBody) });
  } catch (e) {
    if (!hit) throw e;
  }
  return bodies.get(item.id).html;
}

module.exports = { TYPES, items, find, postBody };
