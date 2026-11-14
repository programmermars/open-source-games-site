/* Open Source Games collection: language and theme switches, search, in-page player, table-of-contents highlight. */
(function () {
  "use strict";

  var root = document.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  function isZh() { return root.lang !== "en"; }
  function t(zh, en) { return isZh() ? zh : en; }

  /* ---------- language ---------- */
  var onLangChange = null;
  var langBtn = document.getElementById("lang-toggle");
  langBtn.hidden = false;
  langBtn.addEventListener("click", function () {
    var next = isZh() ? "en" : "zh";
    root.lang = next === "en" ? "en" : "zh-CN";
    store.set("osg-lang", next);
    themeLabel();
    if (onLangChange) onLangChange();
  });

  /* ---------- theme ---------- */
  var themeBtn = document.getElementById("theme-toggle");
  var THEMES = ["auto", "light", "dark"];
  function currentTheme() { return root.getAttribute("data-theme") || "auto"; }
  function themeLabel() {
    var m = { auto: t("主题：自动", "Theme: auto"), light: t("主题：亮", "Theme: light"), dark: t("主题：暗", "Theme: dark") };
    themeBtn.textContent = m[currentTheme()];
  }
  themeBtn.hidden = false;
  themeLabel();
  themeBtn.addEventListener("click", function () {
    var next = THEMES[(THEMES.indexOf(currentTheme()) + 1) % THEMES.length];
    if (next === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", next);
    store.set("osg-theme", next);
    themeLabel();
  });

  /* ---------- everything below exists on the home page only ---------- */
  if (!document.getElementById("catalog")) return;

  /* ---------- search ---------- */
  var q = document.getElementById("q");
  var only = document.getElementById("only-play");
  var countEl = document.getElementById("count");
  var catalog = document.getElementById("catalog");
  var all = Array.prototype.slice.call(catalog.querySelectorAll(".osg-entry"));
  var total = all.length;
  var shown = total;

  function norm(s) {
    return s.toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g, "").trim();
  }
  function selfMatch(li, terms, playOnly) {
    if (playOnly && li.dataset.play !== "1") return false;
    var s = li.dataset.search;
    for (var i = 0; i < terms.length; i++) if (s.indexOf(terms[i]) === -1) return false;
    return true;
  }
  function kidsOf(li) {
    return Array.prototype.slice.call(li.querySelectorAll(":scope > .osg-entries--nested > .osg-entry"));
  }
  function apply() {
    var terms = norm(q.value).split(/\s+/).filter(Boolean);
    var playOnly = only.checked;
    var filtering = terms.length > 0 || playOnly;
    shown = 0;
    catalog.querySelectorAll(".osg-entries:not(.osg-entries--nested) > .osg-entry").forEach(function (li) {
      var me = selfMatch(li, terms, playOnly);
      var kids = kidsOf(li), anyKid = false;
      kids.forEach(function (k) {
        var km = selfMatch(k, terms, playOnly) || (me && !playOnly);
        k.hidden = filtering && !km;
        if (!k.hidden) { anyKid = true; shown++; }
      });
      li.hidden = filtering && !me && !anyKid;
      if (!li.hidden) shown++;
    });
    catalog.querySelectorAll(".osg-entries:not(.osg-entries--nested)").forEach(function (ul) {
      ul.hidden = !ul.querySelector(":scope > .osg-entry:not([hidden])");
    });
    catalog.querySelectorAll(".osg-group").forEach(function (g) {
      g.hidden = !g.querySelector(".osg-entry:not([hidden])");
    });
    catalog.querySelectorAll(".osg-genre").forEach(function (sec) {
      sec.hidden = !sec.querySelector(".osg-entry:not([hidden])");
    });
    updateCount(filtering);
  }
  function updateCount(filtering) {
    if (filtering === undefined) filtering = q.value.trim() !== "" || only.checked;
    if (!filtering) { countEl.textContent = t("共 " + total + " 个项目", total + " projects"); return; }
    countEl.textContent = shown === 0
      ? t("没有匹配的项目。换个词，或取消「只看能直接玩的」。", "Nothing matches. Try another word, or untick “Only browser-playable”.")
      : t("显示 " + shown + " / " + total + " 个项目", "Showing " + shown + " of " + total + " projects");
  }
  var timer;
  q.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(apply, 80); });
  only.addEventListener("change", apply);
  onLangChange = function () { updateCount(); };
  updateCount(false);

  /* ---------- player ---------- */
  var data = {};
  try { data = JSON.parse(document.getElementById("play-data").textContent); } catch (e) {}
  var dlg = document.getElementById("player");
  var frame = document.getElementById("player-frame");
  var titleEl = document.getElementById("player-title");
  var hostEl = document.getElementById("player-host");
  var ctrlEl = document.getElementById("player-controls");
  var newTab = dlg.querySelector('[data-act="newtab"]');
  var canDialog = typeof dlg.showModal === "function";

  function openGame(id) {
    var g = data[id];
    if (!g || g.mode !== "embed" || !canDialog) return false;
    titleEl.textContent = g.title;
    frame.title = g.title;
    frame.src = g.url;
    newTab.href = g.url;
    try { hostEl.textContent = new URL(g.url).hostname; } catch (e) { hostEl.textContent = ""; }
    ctrlEl.textContent = isZh() ? g.controls.zh : g.controls.en;
    if (!dlg.open) dlg.showModal();
    try { history.replaceState(null, "", "#play-" + id); } catch (e) {}
    return true;
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-play-id]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    if (openGame(a.getAttribute("data-play-id"))) e.preventDefault();
  });
  dlg.addEventListener("click", function (e) {
    if (e.target === dlg) dlg.close();
    var act = e.target.closest && e.target.closest("[data-act]");
    if (!act) return;
    var k = act.getAttribute("data-act");
    if (k === "close") dlg.close();
    if (k === "fullscreen") {
      var stage = dlg.querySelector(".player-stage");
      if (stage.requestFullscreen) stage.requestFullscreen().catch(function () {});
    }
    if (k === "newtab") dlg.close();
  });
  dlg.addEventListener("close", function () {
    if (dlg.open) return; /* reopened before this queued event ran */
    frame.src = "about:blank";
    if (location.hash.indexOf("#play-") === 0) {
      try { history.replaceState(null, "", location.pathname + location.search); } catch (e) {}
    }
  });
  if (location.hash.indexOf("#play-") === 0) openGame(location.hash.slice(6));

  /* ---------- table of contents: highlight the genre in view ---------- */
  var links = {};
  document.querySelectorAll(".osg-toc-link").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
  if ("IntersectionObserver" in window) {
    var visible = {};
    var io = new IntersectionObserver(function (items) {
      items.forEach(function (it) { visible[it.target.id] = it.isIntersecting; });
      var first = null;
      catalog.querySelectorAll(".osg-genre").forEach(function (s) { if (!first && visible[s.id]) first = s.id; });
      Object.keys(links).forEach(function (id) {
        if (id === first) links[id].setAttribute("aria-current", "location");
        else links[id].removeAttribute("aria-current");
      });
    }, { rootMargin: "-10% 0px -70% 0px" });
    catalog.querySelectorAll(".osg-genre").forEach(function (s) { io.observe(s); });
  }
})();
