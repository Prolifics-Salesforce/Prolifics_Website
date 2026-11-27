/* Happenings: fills the list page and the detail page from /api/happenings (the HubDB table in HubSpot).
   Text from HubSpot is always set with textContent. Only the Body column is HTML, and the server has cleaned it. */
(function () {
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function parts(ms) { var d = new Date(ms); return { d: d.getUTCDate(), m: MONTHS[d.getUTCMonth()], y: d.getUTCFullYear() }; }
  function longDate(ms) { var p = parts(ms); return p.m + " " + p.d + ", " + p.y; }
  function when(x) {
    if (x.startDate == null) return "";
    if (x.endDate == null || x.endDate <= x.startDate) return longDate(x.startDate);
    return longDate(x.startDate) + " to " + longDate(x.endDate);
  }
  function dateBlock(x) {
    var b = el("span", "hp-d");
    if (x.startDate == null) { b.appendChild(el("b", "", "")); return b; }
    var p = parts(x.startDate); b.appendChild(el("b", "", String(p.d))); b.appendChild(el("span", "", p.m.slice(0, 3) + " " + p.y)); return b;
  }
  function meta(x) {
    var m = el("span", "hp-m"), s = (x.status || "").toLowerCase();
    if (x.type) m.appendChild(el("span", "hp-ty", x.type));
    if (x.location) m.appendChild(el("span", "", x.location));
    if (s === "live" || s === "past") m.appendChild(el("span", "hp-st " + s, s === "live" ? "Live now" : "Past"));
    return m;
  }
  function go(label) { var g = el("span", "hp-go", label + " "); g.appendChild(el("span", "", "→")); return g; }
  function get(url) { return fetch(url, { headers: { Accept: "application/json" } }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, data: j }; }); }); }

  /* ---------------- list page */
  var list = document.getElementById("hp-list");
  if (list) {
    var bar = document.getElementById("hp-filters");
    function row(x) {
      var a = el("a", "hp-i" + (x.featured ? " feat" : "")); a.href = "/happenings/" + encodeURIComponent(x.slug); a.setAttribute("data-type", (x.type || "").toLowerCase());
      if (x.featured) {
        var inn = el("span", "hp-in"), w = when(x); inn.appendChild(meta(x)); if (w) inn.appendChild(el("span", "hp-dl", w));
        inn.appendChild(el("strong", "hp-n", x.name)); if (x.summary) inn.appendChild(el("span", "hp-x", x.summary)); inn.appendChild(go("View details"));
        var ph = el("span", "hp-ph" + (x.image ? " img" : ""));
        if (x.image) { var im = el("img"); im.src = x.image.url; im.alt = x.image.alt || ""; im.loading = "lazy"; ph.appendChild(im); }
        ph.appendChild(dateBlock(x)); a.appendChild(inn); a.appendChild(ph); return a;
      }
      var b = el("span", "hp-b"); b.appendChild(meta(x)); b.appendChild(el("strong", "hp-n", x.name)); if (x.summary) b.appendChild(el("span", "hp-x", x.summary));
      a.appendChild(dateBlock(x)); a.appendChild(b); a.appendChild(go("View details")); return a;
    }
    function filters(items) {
      var seen = {}, types = [];
      items.forEach(function (x) { var k = (x.type || "").toLowerCase(); if (k && !seen[k]) { seen[k] = 1; types.push([k, x.type]); } });
      if (types.length < 2) return;
      [["", "All"]].concat(types).forEach(function (t, i) {
        var c = el("button", "hp-fc", t[1]); c.type = "button"; c.setAttribute("aria-pressed", i === 0 ? "true" : "false");
        c.addEventListener("click", function () {
          [].forEach.call(bar.children, function (o) { o.setAttribute("aria-pressed", o === c ? "true" : "false"); });
          [].forEach.call(list.querySelectorAll(".hp-i"), function (r) { r.hidden = !!t[0] && r.getAttribute("data-type") !== t[0]; });
        });
        bar.appendChild(c);
      });
      bar.hidden = false;
    }
    get("/api/happenings").then(function (r) {
      if (!r.ok) throw new Error("unavailable");
      var items = r.data.items || []; list.textContent = "";
      if (!items.length) { list.appendChild(el("p", "hp-note", "There are no happenings to show right now. Please check back soon.")); return; }
      items.forEach(function (x) { list.appendChild(row(x)); }); filters(items);
    }).catch(function () {
      list.textContent = ""; list.appendChild(el("p", "hp-note", "Happenings could not be loaded. Please try again in a moment."));
    });
  }

  /* ---------------- detail page: the address is /happenings/<slug> */
  var one = document.getElementById("hp-detail");
  if (one) {
    var wait = document.getElementById("hp-wait"), seg = location.pathname.replace(/\/+$/, "").split("/").pop(), slug = "";
    try { slug = decodeURIComponent(seg); } catch (e) { slug = ""; }
    function missing(msg) { wait.textContent = msg + " "; var a = el("a", "", "See all happenings"); a.href = "/happenings"; wait.appendChild(a); }
    if (!slug || slug === "detail" || slug === "happenings") missing("This happening is not available.");
    else get("/api/happenings?slug=" + encodeURIComponent(slug)).then(function (r) {
      if (r.status === 404) return missing("This happening is not available.");
      if (!r.ok) throw new Error("unavailable");
      var x = r.data.item, s = (x.status || "").toLowerCase(), past = s === "past";
      document.title = x.name + " | Prolifics";
      var crumb = document.querySelector(".crumbs [aria-current]"); if (crumb) crumb.textContent = x.name;
      document.getElementById("hp-type").textContent = x.type || "Happening";
      document.getElementById("hp-name").textContent = x.name;
      var dl = document.getElementById("hp-meta");
      [["When", when(x)], ["Where", x.location], ["Status", s === "live" ? "Live now" : past ? "Past" : ""]].forEach(function (p) {
        if (!p[1]) return; var d = el("div"); d.appendChild(el("dt", "", p[0])); d.appendChild(el("dd", "", p[1])); dl.appendChild(d);
      });
      if (!dl.children.length) dl.hidden = true;
      if (x.image) { var f = document.getElementById("hp-fig"), im = el("img"); im.src = x.image.url; im.alt = x.image.alt || ""; f.appendChild(im); f.hidden = false; }
      var sum = document.getElementById("hp-sum"); if (x.summary) sum.textContent = x.summary; else sum.hidden = true;
      document.getElementById("hp-body").innerHTML = x.body || "";
      var reg = document.getElementById("hp-reg");
      if (x.canRegister && !past) {
        reg.querySelector('input[name="happening"]').value = x.slug;
        reg.querySelector("button").textContent = x.buttonText || "Register";
        document.getElementById("hp-reg-h").textContent = x.buttonText || "Register";
        reg.hidden = false;
      } else one.classList.add("solo");
      wait.hidden = true; one.hidden = false;
    }).catch(function () { missing("This happening could not be loaded."); });
  }
})();
