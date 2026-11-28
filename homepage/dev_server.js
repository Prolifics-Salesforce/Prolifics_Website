// Local test server: the built site from dist/ plus the real /api functions (lead form, happenings).
//   node dev_server.js          then open http://localhost:3000/contact
// Settings come from .env.local in this folder (git ignored). The file is read again on every submission, so you can
// edit it without restarting. With HUBSPOT_ACCESS_TOKEN and HUBSPOT_FORM_ID set, a submission here creates a REAL
// contact in HubSpot. Set HUBSPOT_DRY_RUN=1 to test without sending anything.
const http = require("http"), fs = require("fs"), path = require("path");
const ROOT = __dirname, DIST = path.join(ROOT, "dist"), PORT = Number(process.env.PORT) || 3000;
const API = { "/api/lead": require(path.join(ROOT, "src", "api", "lead.js")), "/api/happenings": require(path.join(ROOT, "src", "api", "happenings.js")),
              "/api/resources": require(path.join(ROOT, "src", "api", "resources.js")),
              "/api/sitemap": require(path.join(ROOT, "src", "api", "sitemap.js")) };
const KEYS = ["HUBSPOT_ACCESS_TOKEN", "HUBSPOT_TOKEN", "HUBSPOT_FORM_ID", "HUBSPOT_PORTAL_ID", "HUBSPOT_SUBSCRIPTION_ID", "HUBSPOT_INTEREST_PROPERTY", "HUBSPOT_DRY_RUN", "HUBDB_HAPPENINGS_TABLE", "HUBSPOT_BLOG_ID", "HUBDB_RESOURCES_TABLE"];
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".json": "application/json", ".png": "image/png",
                ".webp": "image/webp", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".css": "text/css" };

function loadEnv() {
  KEYS.forEach((k) => delete process.env[k]);
  let text = "";
  try { text = fs.readFileSync(path.join(ROOT, ".env.local"), "utf8"); } catch { return; }
  text.split(/\r?\n/).forEach((line) => {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*?)\s*$/);
    if (m && KEYS.includes(m[1]) && m[2]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  });
}

http.createServer((req, res) => {
  let url = decodeURIComponent(req.url.split("?")[0]);
  if (url === "/sitemap.xml") { url = "/api/sitemap"; req.url = "/api/sitemap"; }   // same rewrites as dist/vercel.json
  if (url === "/robots.txt") { url = "/api/sitemap"; req.url = "/api/sitemap?file=robots"; }
  const handler = API[url];
  if (handler && req.method !== "POST") {
    loadEnv();
    res.on("finish", () => console.log(req.method + " " + req.url + " -> " + res.statusCode));
    return Promise.resolve(handler(req, res)).catch((e) => { console.error(e); res.statusCode = 500; res.end(); });
  }
  if (/^\/happenings(\/.*)?$/.test(url)) { res.statusCode = 307; res.setHeader("Location", url.replace("/happenings", "/events")); return res.end(); }
  if (/^\/events\/[^/]+\/?$/.test(url)) url = "/events/detail";   // same rewrites as dist/vercel.json
  if (/^\/resources\/article\/[^/]+\/?$/.test(url)) url = "/resources/article";
  if (/^\/resources\/item\/[^/]+\/?$/.test(url)) url = "/resources/item";
  if (handler) {
    let raw = ""; req.on("data", (c) => (raw += c));
    req.on("end", () => {
      loadEnv();
      req.body = raw;   // the function parses JSON and form posts itself
      const mode = process.env.HUBSPOT_DRY_RUN === "1" ? "dry run, nothing sent" : (process.env.HUBSPOT_ACCESS_TOKEN || process.env.HUBSPOT_TOKEN) ? "sending to HubSpot" : "no token set";
      res.on("finish", () => console.log("POST " + url + " -> " + res.statusCode + " (" + mode + ")"));
      Promise.resolve(handler(req, res)).catch((e) => { console.error(e); res.statusCode = 500; res.end(); });
    });
    return;
  }
  let file = path.normalize(path.join(DIST, url));
  if (!file.startsWith(DIST)) { res.statusCode = 403; return res.end(); }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
  if (!fs.existsSync(file)) { res.statusCode = 404; return res.end("Not found"); }
  res.setHeader("Content-Type", TYPES[path.extname(file)] || "application/octet-stream");
  fs.createReadStream(file).pipe(res);
}).listen(PORT, "127.0.0.1", () => console.log("Prolifics site on http://localhost:" + PORT + "/contact"));
