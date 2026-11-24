(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");

  /* hero: rolling banners */
  var kh = $(".khero"), trk = $(".trk"), sl = $$(".sl"), dots = $$(".kdot"), cnt = $(".cnt"), cur = 0, t = null, DUR = 6500;
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function next() { clearTimeout(t); if (!reduce && kh && !kh.classList.contains("paused")) t = setTimeout(function () { go(cur + 1); }, DUR); }
  function go(i) {
    cur = (i + sl.length) % sl.length;
    trk.style.transform = "translateX(" + (-100 * cur) + "%)";
    sl.forEach(function (s, k) { s.classList.toggle("on", k === cur); s.setAttribute("aria-hidden", k !== cur); });
    dots.forEach(function (d, k) { d.classList.remove("on"); d.classList.toggle("done", k < cur); });
    void dots[cur].offsetWidth; dots[cur].classList.add("on");
    cnt.textContent = pad(cur + 1) + " / " + pad(sl.length);
    next();
  }
  if (kh) {
    kh.style.setProperty("--kdur", DUR + "ms");
    dots.forEach(function (d, k) { d.addEventListener("click", function () { go(k); }); });
    $(".arw.prev").addEventListener("click", function () { go(cur - 1); });
    $(".arw.next").addEventListener("click", function () { go(cur + 1); });
    kh.addEventListener("mouseenter", function () { if (fine.matches) { kh.classList.add("paused"); clearTimeout(t); } });
    kh.addEventListener("mouseleave", function () { kh.classList.remove("paused"); next(); });
    var x0 = null;
    kh.addEventListener("pointerdown", function (e) { x0 = e.clientX; });
    kh.addEventListener("pointerup", function (e) { if (x0 === null) return; var dx = e.clientX - x0; x0 = null; if (Math.abs(dx) > 50) go(cur + (dx < 0 ? 1 : -1)); });
    document.addEventListener("keydown", function (e) {
      if (document.activeElement && kh.contains(document.activeElement)) { if (e.key === "ArrowRight") go(cur + 1); if (e.key === "ArrowLeft") go(cur - 1); }
    });
    go(0);
  }

  /* recognition panels */
  var rc = $$(".rc");
  rc.forEach(function (p) {
    function act() { rc.forEach(function (x) { x.classList.toggle("on", x === p); x.setAttribute("aria-expanded", x === p); }); }
    p.addEventListener("click", act); p.addEventListener("focus", act); p.addEventListener("mouseenter", function () { if (fine.matches) act(); });
  });

  /* client stories */
  var ss = $$(".st-sl"), tb = $$(".st-tb"), sc = 0, st = null;
  function sgo(i) { sc = (i + ss.length) % ss.length; ss.forEach(function (s, k) { s.classList.toggle("on", k === sc); }); tb.forEach(function (b, k) { b.classList.toggle("on", k === sc); }); clearTimeout(st); if (!reduce) st = setTimeout(function () { sgo(sc + 1); }, 6500); }
  tb.forEach(function (b, k) { b.addEventListener("click", function () { sgo(k); }); });
  if (ss.length) sgo(0);
})();
