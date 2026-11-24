(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var ease = function (t) { return 1 - Math.pow(1 - t, 3); };
  function tween(ms, fn, done) {
    var t0 = performance.now();
    (function f(now) { var t = Math.min(1, Math.max(0, (now - t0) / ms)); fn(ease(t)); if (t < 1) requestAnimationFrame(f); else if (done) done(); })(t0);
  }

  /* ---------- header: dark over the hero, light after ---------- */
  var hdr = $(".hdr"), hero = $(".hero"), body = document.body;
  function onScroll() { var lim = hero ? hero.offsetHeight - 40 : 40; body.classList.toggle("top", window.scrollY < lim); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- mega menus ---------- */
  var open = null, closeT = null, hoverAt = 0;
  function setMega(btn, show) { btn.setAttribute("aria-expanded", show ? "true" : "false"); document.getElementById(btn.getAttribute("data-mega")).hidden = !show; }
  function closeAll() { $$("[data-mega]").forEach(function (b) { setMega(b, false); }); open = null; }
  $$("[data-mega]").forEach(function (b) {
    var m = document.getElementById(b.getAttribute("data-mega"));
    b.addEventListener("click", function () { if (open === b && Date.now() - hoverAt < 600) return; var was = open === b; closeAll(); if (!was) { setMega(b, true); open = b; } });
    function enter() { if (!fine.matches) return; clearTimeout(closeT); if (open !== b) { closeAll(); setMega(b, true); open = b; hoverAt = Date.now(); } }
    function leave() { if (!fine.matches) return; clearTimeout(closeT); closeT = setTimeout(closeAll, 180); }
    b.addEventListener("mouseenter", enter); b.addEventListener("mouseleave", leave);
    m.addEventListener("mouseenter", function () { clearTimeout(closeT); }); m.addEventListener("mouseleave", leave);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && open) { var b = open; closeAll(); b.focus(); } });
  document.addEventListener("click", function (e) { if (open && !hdr.contains(e.target)) closeAll(); });
  $$(".rail-b").forEach(function (b) {
    function show() {
      $$(".rail-b").forEach(function (x) { x.classList.toggle("on", x === b); });
      $$(".mp").forEach(function (p) { p.hidden = p.id !== b.getAttribute("data-pane"); });
    }
    b.addEventListener("mouseenter", show); b.addEventListener("focus", show); b.addEventListener("click", show);
  });

  /* ---------- hero: 48 counts up, the year runs 1978 to 2026, then the eras play ---------- */
  if (hero) {
    var layers = $$(".n48-l"), outline = $(".n48-o"), washes = $$(".wash"), ticks = $$(".tk"), cap = $(".era-cap"), ct = null;
    var cur = 0, timer = null, DUR = 6500, playing = !reduce, visible = true;
    hero.style.setProperty("--dur", DUR + "ms");
    var setNum = function (v) { var s = (v < 10 ? "0" : "") + v; outline.textContent = s; layers.forEach(function (l) { l.textContent = s; }); };
    var schedule = function () { clearTimeout(timer); if (playing && visible) timer = setTimeout(function () { show(cur + 1); }, DUR); };
    var show = function (i) {
      cur = (i + ticks.length) % ticks.length;
      layers.forEach(function (l, k) { l.classList.toggle("on", k === cur); });
      washes.forEach(function (w, k) { w.classList.toggle("on", k === cur); });
      ticks.forEach(function (t, k) { t.classList.remove("on"); t.classList.toggle("done", k < cur); });
      void ticks[cur].offsetWidth; ticks[cur].classList.add("on");
      var t = ticks[cur];
      cap.classList.add("sw");
      setTimeout(function () {
        $(".era-y", cap).textContent = t.getAttribute("data-y"); $(".era-t", cap).textContent = t.getAttribute("data-t"); $(".era-d", cap).textContent = t.getAttribute("data-d");
        cap.classList.remove("sw");
      }, 300);
      schedule();
    };
    ticks.forEach(function (t, k) { t.addEventListener("click", function () { show(k); }); });
    var eraBox = $(".era");
    eraBox.addEventListener("mouseenter", function () { hero.classList.add("paused"); clearTimeout(timer); });
    eraBox.addEventListener("mouseleave", function () { hero.classList.remove("paused"); schedule(); });
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; hero.classList.toggle("paused", !visible); if (visible) schedule(); else clearTimeout(timer); }, { threshold: 0.15 }).observe(hero);
    if (!reduce) {
      setNum(0);
      tween(2200, function (p) { setNum(Math.round(48 * p)); }, function () { setNum(48); });
      setTimeout(function () { setNum(48); }, 2600);
      var start = (location.hash.match(/era-(\d)/) || [0, 0])[1] | 0;
      setTimeout(function () { show(start); }, 700);
    } else { show(0); }
    window.addEventListener("load", function () { layers.forEach(function (l, k) { if (k) { var im = new Image(); im.src = l.style.backgroundImage.replace(/^url\(["']?|["']?\)$/g, ""); } }); });
  }

  /* ---------- reveal on scroll and count-ups ---------- */
  function countUp(el) {
    var raw = el.getAttribute("data-count"), m = raw.match(/^([^0-9]*)([0-9,.]+)(.*)$/); if (!m || reduce) return;
    var target = parseFloat(m[2].replace(/,/g, "")), comma = m[2].indexOf(",") > -1;
    tween(1600, function (p) { var v = Math.round(target * p); el.textContent = m[1] + (comma ? v.toLocaleString("en-US") : v) + m[3]; }, function () { el.textContent = raw; });
    setTimeout(function () { el.textContent = raw; }, 2000);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("in");
      $$("[data-count]", e.target).forEach(countUp);
      io.unobserve(e.target);
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
  $$("[data-r]").forEach(function (el) { io.observe(el); });

  /* ---------- practices: accordion rows, image follows the cursor ---------- */
  var rows = $$(".pr"), ci = $(".cursor-img"), ciImg = ci && $("img", ci), tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
  rows.forEach(function (r) {
    var b = $(".pr-b", r), p = $(".pr-p", r);
    b.addEventListener("click", function () {
      var opening = !r.classList.contains("open");
      rows.forEach(function (o) { o.classList.remove("open"); $(".pr-b", o).setAttribute("aria-expanded", "false"); $(".pr-p", o).hidden = true; });
      if (opening) { r.classList.add("open"); b.setAttribute("aria-expanded", "true"); p.hidden = false; if (window.innerWidth < 1025) r.scrollIntoView({ behavior: "smooth", block: "start" }); }
      if (ci) ci.classList.remove("on");
    });
    if (ci) {
      b.addEventListener("mouseenter", function () { if (!fine.matches || r.classList.contains("open")) return; ciImg.src = r.getAttribute("data-img"); ci.classList.add("on"); });
      b.addEventListener("mouseleave", function () { ci.classList.remove("on"); });
    }
  });
  var loop = function () { cx += (tx - cx) * 0.18; cy += (ty - cy) * 0.18; ci.style.left = cx + "px"; ci.style.top = cy + "px"; raf = Math.abs(tx - cx) + Math.abs(ty - cy) > 0.5 ? requestAnimationFrame(loop) : null; };
  if (ci) document.addEventListener("mousemove", function (e) { tx = e.clientX + 170; ty = e.clientY; if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });

  /* ---------- solutions: filter and rail arrows ---------- */
  var rail = $(".sc-rail");
  $$(".fc").forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.getAttribute("data-f");
      $$(".fc").forEach(function (x) { x.classList.toggle("on", x === c); x.setAttribute("aria-pressed", x === c); });
      $$(".sc").forEach(function (s) { s.hidden = f !== "all" && s.getAttribute("data-g") !== f; });
      rail.scrollTo({ left: 0 });
    });
  });
  $$(".rn").forEach(function (b) {
    b.addEventListener("click", function () { var card = $(".sc:not([hidden])", rail); rail.scrollBy({ left: (card ? card.offsetWidth + 20 : 380) * parseInt(b.getAttribute("data-d"), 10) * 2 }); });
  });

  /* ---------- case studies: the hovered or focused card widens ---------- */
  $$(".cs-row").forEach(function (row) {
    var cards = $$(".cs", row);
    cards.forEach(function (c) {
      function act() { cards.forEach(function (x) { x.classList.toggle("on", x === c); }); }
      c.addEventListener("mouseenter", function () { if (fine.matches) act(); });
      c.addEventListener("focusin", act); c.addEventListener("click", act);
    });
  });

  /* ---------- mobile drawer ---------- */
  var bur = $(".burger"), dr = document.getElementById("drawer");
  bur.addEventListener("click", function () {
    var show = dr.hidden; dr.style.top = hdr.getBoundingClientRect().bottom + "px";
    dr.hidden = !show; bur.setAttribute("aria-expanded", show); bur.setAttribute("aria-label", show ? "Close menu" : "Open menu");
    document.body.style.overflow = show ? "hidden" : "";
  });
  window.addEventListener("resize", function () { if (window.innerWidth > 1024 && !dr.hidden) bur.click(); });
})();
