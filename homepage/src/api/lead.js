// Vercel serverless function: the lead form posts here and is sent on to the thank-you page.
// build_site.py copies this folder into dist/api, so it deploys with the site at /api/lead. No dependencies.
//
// HubSpot receives the submission in the visitor's browser, through the tracking script on every page ("non-HubSpot
// forms"), so this function sends nothing to HubSpot and stores nothing. It exists because a static page cannot
// accept a POST, and a GET form would put the visitor's details in the address bar.

module.exports = function handler(req, res) {
  res.statusCode = 303;   // "See Other": the browser follows with a GET
  res.setHeader("Location", "/thank-you");
  res.setHeader("Cache-Control", "no-store");
  res.end();
};
