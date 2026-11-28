// Vercel serverless function: the Happenings content for the site, read from the HubDB table in HubSpot.
//   GET /api/happenings              -> { items: [...] }   every visible happening, in display order
//   GET /api/happenings?slug=<slug>  -> { item: {...} }    one happening with its body, or 404
// Answers are cached for about a minute, so an edit published in HubSpot shows on the site within a minute or two.
// The HubSpot form ID and campaign name stay on the server: the browser only learns whether registration is open.
const hubdb = require("./_hubdb.js");

const GUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// The Body column is rich text written in HubSpot. Keep simple formatting only: no scripts, styles, frames, event
// handlers or script links can reach the page.
const TAGS = new Set(["p", "br", "strong", "b", "em", "i", "u", "ul", "ol", "li", "h2", "h3", "h4", "blockquote", "a"]);
function cleanBody(html) {
  let s = String(html || "").trim();
  if (!s) return "";
  if (!/<[a-z][\s\S]*>/i.test(s)) return s.split(/\n\s*\n/).map((p) => "<p>" + esc(p.trim()).replace(/\n/g, "<br>") + "</p>").join("");
  s = s.replace(/<!--[\s\S]*?-->/g, "").replace(/<(script|style|iframe|object|embed|template|svg|math)\b[\s\S]*?<\/\1\s*>/gi, "");
  s = s.replace(/<\/?([a-z][a-z0-9]*)\b([^>]*)>/gi, (m, name, attrs) => {
    const tag = name.toLowerCase(), closing = m[1] === "/";
    if (tag === "h1") return closing ? "</h2>" : "<h2>";
    if (tag === "div") return closing ? "</p>" : "<p>";
    if (!TAGS.has(tag)) return "";
    if (closing) return "</" + tag + ">";
    if (tag !== "a") return "<" + tag + ">";
    const h = attrs.match(/\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/i), url = h ? (h[1] || h[2] || h[3] || "").trim() : "";
    return /^(https?:\/\/|mailto:|\/(?!\/))/i.test(url) ? '<a href="' + esc(url) + '" rel="noopener">' : "<a>";
  });
  return s.replace(/<(?![/a-z])/gi, "&lt;");
}

function view(x, full) {
  const o = { slug: x.slug, name: x.name, type: x.type, location: x.location, summary: x.summary, status: x.status,
              startDate: x.startDate, endDate: x.endDate, featured: x.featured, image: x.image, canRegister: GUID.test(x.formId) };
  if (full) { o.body = cleanBody(x.body); o.buttonText = x.buttonText || "Register"; }
  return o;
}

module.exports = async function handler(req, res) {
  const send = (code, obj, cacheable) => {
    res.statusCode = code;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.setHeader("Cache-Control", cacheable ? "public, s-maxage=60, stale-while-revalidate=300" : "no-store");
    res.end(JSON.stringify(obj));
  };
  if (req.method !== "GET" && req.method !== "HEAD") { res.setHeader("Allow", "GET"); return send(405, { error: "Method not allowed" }); }
  const slug = new URL(req.url, "http://localhost").searchParams.get("slug");
  try {
    if (slug) {
      const row = await hubdb.find(slug);
      return row ? send(200, { item: view(row, true) }, true) : send(404, { error: "Not found" });
    }
    return send(200, { items: (await hubdb.happenings()).map((x) => view(x, false)) }, true);
  } catch (e) {
    console.error("Happenings could not be read: " + e.message);
    return send(502, { error: "Events are not available right now" });
  }
};
