// Vercel serverless function: receives a lead form submission and sends it to HubSpot from the server.
// build_site.py copies this folder into dist/api, so it deploys with the site at /api/lead. No dependencies.
//
// The visitor's details go browser -> this function -> HubSpot Forms API (authenticated). No HubSpot script runs in
// the browser, so ad blockers cannot drop a lead, and only the fields listed in ALLOWED ever leave this function.
//
// Environment variables (Vercel > Project > Settings > Environment Variables):
//   HUBSPOT_ACCESS_TOKEN  required. Service key or private app token with the "forms" scope. Never put it in the
//                       page or the repo. (HUBSPOT_TOKEN is accepted as an older name.)
//   HUBSPOT_FORM_ID     required. ID (GUID) of the HubSpot form that receives the submissions.
//   HUBSPOT_PORTAL_ID   Hub ID. Default 52356695 (Prolifics HubSpot Dev). Set the production ID at launch.
//   HUBSPOT_SUBSCRIPTION_ID   optional, numeric subscription type. When set and the visitor ticks the marketing box,
//                       the opt in is recorded against it.
//   HUBSPOT_INTEREST_PROPERTY optional. Internal name of the contact property for "Area of interest", for example
//                       area_of_interest. When not set, or when HubSpot does not accept the value for that
//                       property, the chosen area is written as the first line of the message instead.
//   HUBSPOT_DRY_RUN     "1" returns the payload without calling HubSpot (for local testing).
//
// The HubSpot form must have reCAPTCHA off: HubSpot rejects server submissions otherwise.
// Nothing a visitor typed is written to the logs: errors log the HubSpot status and error types only.
//
// Requests: JSON { fields: {...}, context: { pageUri, pageName } } from pages.js, answered with JSON; or a plain form
// post (visitor without JavaScript), answered with a redirect to /thank-you.

const ALLOWED = ["firstname", "lastname", "email", "phone", "company", "jobtitle", "country", "message"];   // default HubSpot contact properties
const MAX = { message: 5000 };
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/;

function clean(v, max) { return v == null ? "" : String(v).trim().slice(0, max || 500); }

async function post(url, token, payload) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
    body: JSON.stringify(payload),
  });
  const body = r.ok ? {} : await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, types: (body.errors || []).map((e) => e.errorType) };
}

module.exports = async function handler(req, res) {
  const isForm = /application\/x-www-form-urlencoded/i.test(req.headers["content-type"] || "");
  const reply = (code, obj) => {
    res.setHeader("Cache-Control", "no-store");
    if (isForm) {   // no JavaScript in the browser: answer with a page, not JSON
      res.statusCode = 303; res.setHeader("Location", code === 200 ? "/thank-you" : "/contact"); return res.end();
    }
    res.statusCode = code; res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(obj));
  };

  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return reply(405, { ok: false, error: "Method not allowed" }); }

  // Only this site's own pages may post here.
  const origin = req.headers.origin, host = req.headers["x-forwarded-host"] || req.headers.host;
  if (origin && origin !== "https://" + host && origin !== "http://" + host) return reply(403, { ok: false, error: "Origin not allowed" });

  let body = req.body, input, ctx = {};
  if (typeof body === "string") {
    if (isForm) body = Object.fromEntries(new URLSearchParams(body));
    else { try { body = JSON.parse(body); } catch { body = null; } }
  }
  if (isForm) input = body;
  else { input = body && body.fields; ctx = (body && body.context) || {}; }
  if (!input || typeof input !== "object" || Array.isArray(input)) return reply(400, { ok: false, error: "Expected form fields" });

  // Honeypot: bots fill the hidden field. Answer as if it worked, send nothing.
  if (input.website_url) return reply(200, { ok: true });

  const v = {};
  for (const n of ALLOWED) { const x = clean(input[n], MAX[n]); if (x) v[n] = x; }
  if (!v.firstname || !v.lastname) return reply(400, { ok: false, error: "First and last name are required" });
  if (!EMAIL.test(v.email || "")) return reply(400, { ok: false, error: "A valid email is required" });

  const interest = clean(input.interest, 80), prop = process.env.HUBSPOT_INTEREST_PROPERTY;
  const toFields = (asProperty) => {
    const f = Object.assign({}, v);
    if (interest && asProperty) f[prop] = interest;
    else if (interest) f.message = ("Area of interest: " + interest + (v.message ? "\n\n" + v.message : "")).slice(0, MAX.message);
    return Object.keys(f).map((name) => ({ objectTypeId: "0-1", name, value: f[name] }));
  };

  // HubSpot answers 200 but silently discards a submission whose page address is on a shared preview host
  // (*.vercel.app): tested 25 Nov 2026, localhost and prolifics.com addresses were kept. On those hosts the address
  // goes into the page name instead, so preview deployments can be tested. A real domain is sent normally.
  let pageUri = clean(ctx.pageUri || req.headers.referer, 2000), pageName = clean(ctx.pageName, 300);
  if (/^https?:\/\/[^\/]*\.vercel\.app(\/|$)/i.test(pageUri)) {
    pageName = ((pageName ? pageName + " " : "") + "(" + pageUri.replace(/^https?:\/\//i, "").split(/[?#]/)[0] + ")").slice(0, 300);
    pageUri = "";
  }

  const payload = {
    submittedAt: Date.now(),
    fields: toFields(Boolean(prop)),
    context: {
      pageUri: pageUri || undefined,
      pageName: pageName || undefined,
      ipAddress: (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || undefined,
    },
  };
  const sub = Number(process.env.HUBSPOT_SUBSCRIPTION_ID), optIn = ["true", "on"].includes(String(input.marketing_opt_in));
  const consent = {
    consentToProcess: true, text: "I agree that Prolifics may use these details to respond to my request.",
    communications: sub && optIn ? [{ value: true, subscriptionTypeId: sub, text: "Send me Prolifics insights and event invitations." }] : [],
  };
  if (sub && optIn) payload.legalConsentOptions = { consent };

  if (process.env.HUBSPOT_DRY_RUN === "1") return reply(200, { ok: true, dryRun: true, payload });

  const token = process.env.HUBSPOT_ACCESS_TOKEN || process.env.HUBSPOT_TOKEN, formId = process.env.HUBSPOT_FORM_ID, portal = process.env.HUBSPOT_PORTAL_ID || "52356695";
  if (!token || !formId) {
    console.error("Lead form is not configured: set HUBSPOT_ACCESS_TOKEN and HUBSPOT_FORM_ID.");
    return reply(500, { ok: false, error: "The form is not configured" });
  }
  const url = "https://api.hsforms.com/submissions/v3/integration/secure/submit/" + portal + "/" + formId;
  try {
    let r = await post(url, token, payload);
    if (!r.ok && r.types.some((t) => /^MISSING_PROCESSING_CONSENT/.test(t)) && !payload.legalConsentOptions) {
      // The HubSpot form has consent options turned on. The visitor accepted the notice under the button: say so.
      payload.legalConsentOptions = { consent };
      r = await post(url, token, payload);
    }
    if (!r.ok && interest && prop && r.status === 400) {
      // HubSpot refused the area of interest as a property (unknown property or value): keep the lead, put it in the message.
      console.warn("HubSpot did not accept " + prop + " (" + r.types.join(", ") + "); sending the area of interest in the message.");
      payload.fields = toFields(false);
      r = await post(url, token, payload);
    }
    if (r.ok) return reply(200, { ok: true });
    console.error("HubSpot rejected a submission: status " + r.status + ", " + (r.types.join(", ") || "no error type"));
    return reply(r.status === 429 ? 503 : 502, { ok: false, error: "HubSpot did not accept the submission" });
  } catch (e) {
    console.error("HubSpot request failed: " + (e && e.name));
    return reply(502, { ok: false, error: "Could not reach HubSpot" });
  }
};
