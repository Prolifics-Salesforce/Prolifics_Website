/* Inner pages: highlight the current section in the sticky sub navigation and the sidebar table of contents. */
(function () {
  var links = [].slice.call(document.querySelectorAll(".subnav ul a, .toc a"));
  if (!links.length || !("IntersectionObserver" in window)) return;
  var byId = {};
  links.forEach(function (a) { var id = a.getAttribute("href").slice(1); (byId[id] = byId[id] || []).push(a); });
  var secs = Object.keys(byId).map(function (id) { return document.getElementById(id); }).filter(Boolean);
  var current = null;
  function set(id) {
    if (id === current) return; current = id;
    links.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + id); });
    var on = document.querySelector(".subnav ul a.on");
    if (on && on.scrollIntoView && window.innerWidth < 1025) { var ul = on.parentNode.parentNode; ul.scrollTo({ left: on.offsetLeft - 16, behavior: "smooth" }); }
  }
  var io = new IntersectionObserver(function () {
    var best = null;
    secs.forEach(function (s) { var t = s.getBoundingClientRect().top; if (t < window.innerHeight * 0.35) best = s.id; });
    set(best);
  }, { threshold: [0, 0.25, 0.5, 1], rootMargin: "0px 0px -40% 0px" });
  secs.forEach(function (s) { io.observe(s); });
  window.addEventListener("scroll", function () {
    var best = null;
    secs.forEach(function (s) { if (s.getBoundingClientRect().top < window.innerHeight * 0.35) best = s.id; });
    set(best);
  }, { passive: true });
})();
/* Service explorer: accessible tabs (click, arrow keys, Home and End). */
(function () {
  [].forEach.call(document.querySelectorAll(".cx"), function (cx) {
    var tabs = [].slice.call(cx.querySelectorAll(".cx-t"));
    function sel(t, focus) {
      tabs.forEach(function (x) {
        var on = x === t; x.setAttribute("aria-selected", on); x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) t.focus();
      if (window.innerWidth < 1025) t.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { sel(t); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = tabs.length, j = null;
        if (k === "ArrowDown" || k === "ArrowRight") j = (i + 1) % n;
        else if (k === "ArrowUp" || k === "ArrowLeft") j = (i - 1 + n) % n;
        else if (k === "Home") j = 0; else if (k === "End") j = n - 1;
        if (j !== null) { e.preventDefault(); sel(tabs[j], true); }
      });
    });
  });
})();
/* Filter chips (solutions, locations, resources): show cards whose data-g matches. */
(function () {
  [].forEach.call(document.querySelectorAll(".fcs2"), function (bar) {
    var list = bar.nextElementSibling;
    [].forEach.call(bar.querySelectorAll(".fc2"), function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-f");
        [].forEach.call(bar.querySelectorAll(".fc2"), function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b); });
        [].forEach.call(list.querySelectorAll("[data-g]"), function (c) { c.hidden = f !== "all" && c.getAttribute("data-g") !== f; if (!c.hidden) c.classList.add("in"); });
      });
    });
  });
})();
/* Lead forms: check the three required fields, post to /api/lead (which sends to HubSpot from the server), show the
   result inline. Without JavaScript the form posts normally and the server redirects to /thank-you. */
(function () {
  [].forEach.call(document.querySelectorAll("form.lf"), function (f) {
    var msg = f.querySelector(".lf-m"), btn = f.querySelector("button");
    f.noValidate = true;   // this script shows its own messages
    function err(i, t) { i.setAttribute("aria-invalid", t ? "true" : "false"); i.parentNode.querySelector(".lf-e").textContent = t; }
    f.addEventListener("input", function (e) { if (e.target.getAttribute("aria-invalid") === "true") err(e.target, ""); });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = null, fields = {};
      [].forEach.call(f.elements, function (i) {
        if (!i.name) return;
        var v = i.type === "checkbox" ? (i.checked ? "true" : "") : i.value.trim();
        if (i.required) {
          var t = !v ? "This field is required" : (i.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v)) ? "Enter a valid email address" : "";
          err(i, t); if (t && !bad) bad = i;
        }
        if (v) fields[i.name] = v;
      });
      if (bad) { bad.focus(); return; }
      btn.disabled = true; msg.className = "lf-m"; msg.textContent = "Sending your request";
      fetch("/api/lead", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fields: fields, context: { pageUri: location.href, pageName: document.title } }) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.ok) throw new Error("rejected"); }); })
        .then(function () {
          var ok = document.createElement("div"), h = document.createElement("h3"), t = document.createElement("div");
          ok.className = "lf-ok"; ok.setAttribute("role", "status"); ok.tabIndex = -1; h.textContent = "Thank you";
          t.textContent = f.getAttribute("data-ok") || "A Prolifics expert in your industry and platform will get back to you within one business day.";
          ok.appendChild(h); ok.appendChild(t); f.innerHTML = ""; f.appendChild(ok);
          f.firstChild.focus();
        })
        .catch(function () {
          btn.disabled = false; msg.className = "lf-m bad";
          msg.textContent = "We could not send your request. Please try again, or call us on the numbers on the contact page.";
        });
    });
  });
})();
