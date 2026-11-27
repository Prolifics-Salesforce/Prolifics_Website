// Shared reader for the "Happenings" HubDB table. The leading underscore keeps Vercel from exposing this file as a
// route; happenings.js and lead.js require it.
//
// Marketing edits the table in HubSpot (Content > HubDB > Happenings) and publishes it. The site reads the published
// rows from the server with HUBSPOT_ACCESS_TOKEN (scopes hubdb.rows.read, hubdb.tables.read). Public API access on the
// table is off, so the browser can never read it directly.
//
// Environment variables:
//   HUBSPOT_ACCESS_TOKEN     required (the same key the lead form uses)
//   HUBDB_HAPPENINGS_TABLE   table name or ID, default "happenings"

const TTL = 60 * 1000;   // HubSpot is asked at most once a minute per server instance
let cache = { at: 0, rows: null };

const text = (v) => (v == null ? "" : String(v).trim());
const date = (v) => (typeof v === "number" && isFinite(v) ? v : (v && !isNaN(Date.parse(v)) ? Date.parse(v) : null));

function normalize(row) {
  const v = row.values || {}, img = v.image && typeof v.image === "object" ? v.image : null;
  const opt = (x) => text(x && typeof x === "object" ? (x.label || x.name) : x);   // text today, dropdown-safe later
  return {
    slug: text(v.slug).toLowerCase(), name: text(v.name), type: opt(v.type), location: text(v.location), summary: text(v.summary),
    buttonText: text(v.button_text), formId: text(v.form_id), campaign: text(v.campaign), status: opt(v.status),
    startDate: date(v.start_date), endDate: date(v.end_date), featured: v.featured === 1 || v.featured === true,
    body: text(v.body),
    image: img && /^https:\/\//i.test(text(img.url)) ? { url: text(img.url), alt: text(img.altText), width: img.width || null, height: img.height || null } : null,
  };
}

// Featured first; then live, upcoming and anything else by start date, soonest first; past ones last, newest first.
function order(a, b) {
  if (a.featured !== b.featured) return a.featured ? -1 : 1;
  const past = (x) => /^past$/i.test(x.status), pa = past(a), pb = past(b);
  if (pa !== pb) return pa ? 1 : -1;
  const da = a.startDate == null ? Infinity : a.startDate, db = b.startDate == null ? Infinity : b.startDate;
  return pa ? db - da : da - db;
}

async function fetchRows() {
  const token = process.env.HUBSPOT_ACCESS_TOKEN || process.env.HUBSPOT_TOKEN;
  if (!token) throw new Error("HUBSPOT_ACCESS_TOKEN is not set");
  const table = encodeURIComponent(process.env.HUBDB_HAPPENINGS_TABLE || "happenings");
  const out = [];
  let after = "";
  for (let page = 0; page < 10; page++) {
    const r = await fetch("https://api.hubapi.com/cms/v3/hubdb/tables/" + table + "/rows?limit=200" + (after ? "&after=" + encodeURIComponent(after) : ""),
      { headers: { Authorization: "Bearer " + token } });
    if (!r.ok) throw new Error("HubDB read failed with status " + r.status);
    const j = await r.json();
    (j.results || []).forEach((row) => out.push(normalize(row)));
    after = j.paging && j.paging.next && j.paging.next.after;
    if (!after) break;
  }
  // A row needs a name and a slug to be shown. Status "Hidden" (any letter case) takes it off the site.
  return out.filter((x) => x.name && /^[a-z0-9][a-z0-9-]*$/.test(x.slug) && !/^hidden$/i.test(x.status)).sort(order);
}

// Published rows, ready to show. If HubSpot is unreachable, the last good copy is served.
async function happenings() {
  if (cache.rows && Date.now() - cache.at < TTL) return cache.rows;
  try {
    cache = { at: Date.now(), rows: await fetchRows() };
  } catch (e) {
    if (!cache.rows) throw e;
    console.error("Happenings: serving the last good copy. " + e.message);
  }
  return cache.rows;
}

async function find(slug) {
  const s = text(slug).toLowerCase();
  return (await happenings()).find((x) => x.slug === s) || null;
}

module.exports = { happenings, find };
