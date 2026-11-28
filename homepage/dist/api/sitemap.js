// Vercel serverless function: the sitemap and the robots file, for Google Search Console and other search engines.
//   GET /sitemap.xml   (rewritten to /api/sitemap)                every page of the site
//   GET /robots.txt    (rewritten to /api/sitemap?file=robots)    allows crawling, the API included, and names the sitemap
// The list is made of the pages built into the site (_paths.json, written by build_site.py) plus what is live in
// HubSpot right now: every article, one pager and video in the Resources library and every event. A post published
// in HubSpot is in the sitemap within minutes. If HubSpot cannot be read, the built pages are still listed.
// Addresses use the host the request came in on, so the same code works on the temporary address and the real domain.
const resources = require("./_resources.js");
const hubdb = require("./_hubdb.js");
let PATHS = ["/"];
try { PATHS = require("./_paths.json"); } catch (e) { /* not built yet: the home page only */ }

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;" }[c]));

module.exports = async function handler(req, res) {
  if (req.method !== "GET" && req.method !== "HEAD") { res.statusCode = 405; res.setHeader("Allow", "GET"); return res.end(); }
  const host = String(req.headers["x-forwarded-host"] || req.headers.host || "").replace(/[^a-z0-9.:-]/gi, "");
  const base = (/^(localhost|127\.0\.0\.1)(:|$)/.test(host) ? "http://" : "https://") + host;
  res.setHeader("Cache-Control", "public, s-maxage=300");

  if (new URL(req.url, "http://localhost").searchParams.get("file") === "robots") {
    res.statusCode = 200; res.setHeader("Content-Type", "text/plain; charset=utf-8");
    // /api is left open: Google has to fetch /api/resources and /api/happenings to render the article and event pages.
    // The API answers carry an X-Robots-Tag noindex header (dist/vercel.json), so the data itself is not listed.
    return res.end("User-agent: *\nAllow: /\n\nSitemap: " + base + "/sitemap.xml\n");
  }

  const urls = PATHS.map((p) => ({ loc: p }));
  const [lib, events] = await Promise.allSettled([resources.items(), hubdb.happenings()]);
  if (lib.status === "fulfilled") lib.value.forEach((x) => urls.push({ loc: (x.kind === "post" ? "/resources/article/" : "/resources/item/") + x.slug, lastmod: x.date }));
  else console.error("Sitemap: the library could not be read. " + lib.reason.message);
  if (events.status === "fulfilled") events.value.forEach((x) => urls.push({ loc: "/events/" + x.slug }));
  else console.error("Sitemap: events could not be read. " + events.reason.message);

  const xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + urls.map((u) => "  <url><loc>" + esc(base + u.loc) + "</loc>" + (u.lastmod ? "<lastmod>" + esc(u.lastmod) + "</lastmod>" : "") + "</url>").join("\n")
    + "\n</urlset>\n";
  res.statusCode = 200; res.setHeader("Content-Type", "application/xml; charset=utf-8");
  res.end(xml);
};
