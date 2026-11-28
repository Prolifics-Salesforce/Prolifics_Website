/* Resource Center library: fills the list on /resources and the article and item pages from /api/resources (HubSpot blog
   and table). Text is always set with textContent. Only the body is HTML, and the server has cleaned it.
   Every card opens a page on this site: /resources/article/<slug> for a post, /resources/item/<slug> for a one pager
   or a video. Nothing here sends a visitor to another site. */
(function () {
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function longDate(s) { var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s || ""); return m ? MONTHS[+m[2] - 1] + " " + +m[3] + ", " + m[1] : ""; }
  function get(url) { return fetch(url, { headers: { Accept: "application/json" } }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, data: j }; }); }); }
  function card(x) {
    var a = el("a", "rs-c"); a.href = x.path && x.path.charAt(0) === "/" ? x.path : "/resources/article/" + encodeURIComponent(x.slug);
    var im = el("span", "rs-im" + (x.video ? " vid" : ""));
    if (x.image) { var i = el("img"); i.src = x.image.thumb || x.image.url; i.alt = ""; i.loading = "lazy"; im.appendChild(i); }
    var b = el("span", "rs-b"), m = el("span", "rs-m");
    if (x.type) m.appendChild(el("span", "rs-ty", x.type.label));
    var d = longDate(x.date); if (d) m.appendChild(el("span", "", d));
    b.appendChild(m); b.appendChild(el("strong", "rs-n", x.title)); if (x.excerpt) b.appendChild(el("span", "rs-x", x.excerpt));
    var g = el("span", "rs-go", (x.video ? "Watch" : x.type && x.type.slug === "one-pager" ? "View" : "Read") + " "); g.appendChild(el("span", "", "→")); b.appendChild(g);
    a.appendChild(im); a.appendChild(b); return a;
  }

  /* ---------------- list on the Resources page */
  var list = document.getElementById("rs-list");
  if (list) {
    var bar = document.getElementById("rs-filters"), form = document.getElementById("rs-search"), box = document.getElementById("rs-q"),
        more = document.getElementById("rs-more"), count = document.getElementById("rs-count");
    var qs = new URLSearchParams(location.search), st = { type: (qs.get("type") || "").toLowerCase(), q: (qs.get("q") || "").slice(0, 80), page: 1, pages: 1, shown: 0 }, run = 0, chips = false;
    box.value = st.q;
    /* A type link from the menu shows that type: the heading names it and the page lands on the library. */
    var ALIAS = { "case-studies": "case-study", "one-pagers": "one-pager", blogs: "blog", videos: "video", "planning-guides": "planning-guide" };
    var NAMES = { blog: "Blogs", news: "News", "case-study": "Case Studies", "planning-guide": "Planning Guides", "one-pager": "One Pagers", video: "Videos" };
    st.type = ALIAS[st.type] || st.type;
    var lib = document.getElementById("library"), head = lib ? lib.querySelector("h2") : null, headText = head ? head.textContent : "", landed = !st.type;
    function title() { if (head) head.textContent = NAMES[st.type] ? NAMES[st.type] + " from Prolifics" : headText; }
    function land() { if (landed) return; landed = true; if (lib && lib.scrollIntoView) lib.scrollIntoView(); }
    title();
    function note(msg) { list.textContent = ""; list.appendChild(el("p", "rs-note", msg)); }
    function address() {
      var p = new URLSearchParams(); if (st.type) p.set("type", st.type); if (st.q) p.set("q", st.q);
      var s = p.toString(); history.replaceState(null, "", location.pathname + (s ? "?" + s : "") + "#library");
    }
    function press() { [].forEach.call(bar.children, function (c) { c.setAttribute("aria-pressed", c.getAttribute("data-t") === st.type ? "true" : "false"); }); }
    function buildChips(types) {
      if (chips || !types || !types.length) return; chips = true;
      [{ slug: "", label: "All" }].concat(types).forEach(function (t) {
        var c = el("button", "rs-fc", t.label); c.type = "button"; c.setAttribute("data-t", t.slug);
        c.addEventListener("click", function () { if (st.type === t.slug) return; st.type = t.slug; title(); address(); load(true); });
        bar.appendChild(c);
      });
      bar.hidden = false;
    }
    function load(fresh) {
      var mine = ++run;
      if (fresh) { st.page = 1; st.shown = 0; note("Loading"); count.textContent = ""; more.hidden = true; }
      else { more.disabled = true; more.textContent = "Loading"; }
      var u = "/api/resources?page=" + st.page + (st.type ? "&type=" + encodeURIComponent(st.type) : "") + (st.q ? "&q=" + encodeURIComponent(st.q) : "");
      get(u).then(function (r) {
        if (mine !== run) return;
        if (!r.ok) throw new Error("unavailable");
        var d = r.data, items = d.items || [];
        buildChips(d.types); press(); land();
        if (fresh) list.textContent = "";
        if (fresh && !items.length) {
          note(st.q ? "Nothing matches that search. Try a different word." : st.type ? "There is nothing of this type yet. Please check back soon." : "New resources are on the way. Please check back soon.");
          form.hidden = !st.q && !st.type; return;
        }
        form.hidden = false;
        items.forEach(function (x) { list.appendChild(card(x)); });
        st.pages = d.pages || 1; st.shown += items.length;
        count.textContent = "Showing " + st.shown + " of " + (d.total || st.shown);
        more.disabled = false; more.textContent = "Load more"; more.hidden = st.page >= st.pages;
      }).catch(function () {
        if (mine !== run) return;
        if (fresh) note("The library could not be loaded. Please try again in a moment.");
        else { st.page--; more.disabled = false; more.textContent = "Load more"; }
      });
    }
    form.addEventListener("submit", function (e) { e.preventDefault(); st.q = box.value.trim().slice(0, 80); address(); load(true); });
    more.addEventListener("click", function () { st.page++; load(false); });
    load(true);
  }

  /* ---------------- article and item pages: the address is /resources/article/<slug> or /resources/item/<slug> */
  var one = document.getElementById("rs-article");
  if (one) {
    var wait = document.getElementById("rs-wait"), seg = location.pathname.replace(/\/+$/, "").split("/").pop(), slug = "";
    try { slug = decodeURIComponent(seg); } catch (e) { slug = ""; }
    function missing(msg) { wait.textContent = msg + " "; var a = el("a", "", "See all resources"); a.href = "/resources#library"; wait.appendChild(a); }
    if (!slug || slug === "article" || slug === "item") missing("This resource is not available.");
    else get("/api/resources?slug=" + encodeURIComponent(slug)).then(function (r) {
      if (r.status === 404) return missing("This resource is not available.");
      if (!r.ok) throw new Error("unavailable");
      var x = r.data.item;
      document.title = x.title + " | Prolifics";
      var crumb = document.querySelector(".crumbs [aria-current]"); if (crumb) crumb.textContent = x.title;
      document.getElementById("rs-type").textContent = x.type ? x.type.label : "Resource";
      document.getElementById("rs-title").textContent = x.title;
      var d = longDate(x.date), when = document.getElementById("rs-date"); if (d) when.textContent = d; else when.hidden = true;
      var f = document.getElementById("rs-fig"), body = document.getElementById("rs-body"), sum = document.getElementById("rs-sum");
      if (x.summary && sum) { sum.textContent = x.summary; sum.hidden = false; }   // one pagers and videos lead with their summary
      if (x.video) {   // the id is 11 letters, digits, hyphens or underscores, checked on the server
        var fr = el("iframe"); fr.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(x.video); fr.title = x.title; fr.loading = "lazy";
        fr.allow = "accelerometer; encrypted-media; picture-in-picture; fullscreen"; fr.allowFullscreen = true; fr.referrerPolicy = "strict-origin-when-cross-origin";
        f.className += " vid"; f.appendChild(fr); f.hidden = false;
      } else if (x.image) { var im = el("img"); im.src = x.image.url; im.alt = x.image.alt || ""; f.appendChild(im); f.hidden = false; }
      body.innerHTML = x.body || "";
      if (x.file && /^https:\/\//i.test(x.file)) {   // the file stays a download from this page
        var o = el("a", "btn btn-p rs-open", "Download"); o.href = x.file; o.setAttribute("download", ""); o.rel = "noopener";
        body.parentNode.insertBefore(o, body.nextSibling);
      }
      wait.hidden = true; one.hidden = false;
      if (!x.type) return;
      get("/api/resources?type=" + encodeURIComponent(x.type.slug)).then(function (m) {
        var rest = ((m.ok && m.data.items) || []).filter(function (y) { return y.slug !== x.slug; }).slice(0, 3);
        if (!rest.length) return;
        var grid = document.getElementById("rs-rel-list"); rest.forEach(function (y) { grid.appendChild(card(y)); });
        document.getElementById("rs-rel-h").textContent = "More " + x.type.label.toLowerCase();
        document.getElementById("rs-rel").hidden = false;
      }).catch(function () {});
    }).catch(function () { missing("This resource could not be loaded."); });
  }
})();
