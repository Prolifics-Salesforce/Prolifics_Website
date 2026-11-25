// Vercel serverless function: receives a website form submission and forwards it to HubSpot.
// build_site.py copies this folder into dist/api, so it deploys with the site at /api/lead. No dependencies.
//
// Environment variables (Vercel project settings):
//   HUBSPOT_TOKEN       private app token with the "forms" scope. When set, the authenticated "secure" endpoint is
//                       used. Recommended: without it HubSpot rejects any field that is not on the form definition
//                       (FIELD_NOT_IN_FORM_DEFINITION), and this function then resends the core fields only
//                       (first name, last name, email, phone) so the lead is not lost.
//                       reCAPTCHA must stay off on the HubSpot forms: HubSpot rejects server submissions otherwise.
//   HUBSPOT_SUBSCRIPTION_ID  optional numeric subscription type. When set and the visitor ticks the marketing box,
//                       the opt in is recorded against that subscription.
//   HUBSPOT_PORTAL_ID   default 8077126
//   ALLOWED_ORIGINS     optional, comma separated. Only needed if another site posts here.
//   HUBSPOT_DRY_RUN     "1" returns the payload without calling HubSpot (use this while testing)
//
// Request (JSON):  { formKey: "sf", fields: { firstname: "...", email: "..." }, context: { pageUri, pageName } }
// Response:        { ok: true } or { ok: false, error }

// "Website 2026: <practice>" forms. Repeated in src/build_pages.py (FORMS): keep the two in step.
const FORMS = {
  ai: "44477275-4b25-44a6-8d63-35ab5b1805ad", fde: "09cebf58-d31b-4789-8594-8d75016fdc52",
  sf: "770410e5-bbd4-4488-bcf0-7b0e2cb8d6bb", sn: "d9261c64-8c64-47cd-b4f9-df15365f0157",
  sap: "1b72d9b5-c1b7-470a-83d0-83dca7968c11", app: "23ff4485-d0aa-46f6-98fb-45e17784110b",
  bt: "e4b0d1cd-bb32-43cb-8b78-d0dd0f6ef5fc", qe: "10fb9988-1b78-47f8-af87-f864e2ee42f2",
  solutions: "d3e700db-c885-421e-99f8-caf567f4b21e", general: "a63a4cb4-4803-4425-b135-ddbf740dfa43",
};

// Only these are forwarded. All are default HubSpot contact properties, so nothing has to be created in the portal.
const ALLOWED = new Set(["firstname", "lastname", "email", "phone", "company", "jobtitle", "country", "message"]);
const CORE = new Set(["firstname", "lastname", "email", "phone"]);   // the fields on the forms as created
const MAX = { message: 5000 };
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/;

function cors(req, res) {
  const allowed = (process.env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const origin = req.headers.origin;
  if (origin && allowed.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  }
  // The site's own pages always pass. Another origin must be on the list.
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  return !origin || origin === "https://" + host || origin === "http://" + host || allowed.includes(origin);
}

function cookie(req, name) {
  const m = (req.headers.cookie || "").match(new RegExp("(?:^|;\\s*)" + name + "=([^;]+)"));
  return m ? decodeURIComponent(m[1]) : undefined;
}

async function send(url, token, payload) {
  const r = await fetch(url, {
    method: "POST",
    headers: Object.assign({ "Content-Type": "application/json" }, token ? { Authorization: "Bearer " + token } : {}),
    body: JSON.stringify(payload),
  });
  const details = r.ok ? {} : await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, details };
}

module.exports = async function handler(req, res) {
  const originOk = cors(req, res);
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ ok: false, error: "Method not allowed" });
  if (!originOk) return res.status(403).json({ ok: false, error: "Origin not allowed" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = null; } }
  if (!body || !body.fields || typeof body.fields !== "object" || Array.isArray(body.fields)) {
    return res.status(400).json({ ok: false, error: "Expected JSON with a fields object" });
  }

  // Honeypot: bots fill the hidden field. Answer 200 so they learn nothing, send nothing.
  if (body.fields.website_url) return res.status(200).json({ ok: true });

  const fields = [];
  for (const [name, raw] of Object.entries(body.fields)) {
    if (!ALLOWED.has(name) || raw == null) continue;
    const value = String(raw).trim().slice(0, MAX[name] || 500);
    if (value) fields.push({ objectTypeId: "0-1", name, value });
  }
  const get = (n) => (fields.find((f) => f.name === n) || {}).value;
  if (!get("firstname") || !get("lastname")) return res.status(400).json({ ok: false, error: "First and last name are required" });
  if (!EMAIL.test(get("email") || "")) return res.status(400).json({ ok: false, error: "A valid email is required" });

  const guid = FORMS[body.formKey] || FORMS.general;
  const portal = process.env.HUBSPOT_PORTAL_ID || "8077126";
  const ctx = body.context || {};
  const context = {
    pageUri: String(ctx.pageUri || req.headers.referer || "").slice(0, 2000) || undefined,
    pageName: String(ctx.pageName || "").slice(0, 300) || undefined,
    hutk: cookie(req, "hubspotutk"),
    ipAddress: (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || undefined,
  };
  const payload = { submittedAt: Date.now(), fields, context };
  const sub = Number(process.env.HUBSPOT_SUBSCRIPTION_ID);
  if (sub && String(body.fields.marketing_opt_in) === "true") {
    payload.legalConsentOptions = { consent: {
      consentToProcess: true, text: "I agree that Prolifics may use these details to respond to my request.",
      communications: [{ value: true, subscriptionTypeId: sub, text: "Send me Prolifics insights and event invitations." }] } };
  }

  if (process.env.HUBSPOT_DRY_RUN === "1") return res.status(200).json({ ok: true, dryRun: true, form: guid, payload });

  const token = process.env.HUBSPOT_TOKEN;
  const url = "https://api.hsforms.com/submissions/v3/integration/" + (token ? "secure/" : "") + "submit/" + portal + "/" + guid;
  try {
    let r = await send(url, token, payload);
    const types = (r.details.errors || []).map((e) => e.errorType);
    if (!r.ok && r.status === 400 && types.includes("FIELD_NOT_IN_FORM_DEFINITION")) {
      // The HubSpot form does not carry the extra fields yet. Keep the lead: resend the core fields only.
      console.warn("HubSpot form " + guid + " lacks some fields; resending core fields only. Set HUBSPOT_TOKEN or add the fields to the form.");
      r = await send(url, token, Object.assign({}, payload, { fields: fields.filter((f) => CORE.has(f.name)) }));
      if (r.ok) return res.status(200).json({ ok: true, partial: true });
    }
    if (r.ok) return res.status(200).json({ ok: true });
    console.error("HubSpot rejected submission", r.status, JSON.stringify(r.details));
    return res.status(r.status === 429 ? 503 : 502).json({ ok: false, error: "HubSpot did not accept the submission" });
  } catch (e) {
    console.error("HubSpot request failed", e);
    return res.status(502).json({ ok: false, error: "Could not reach HubSpot" });
  }
};
