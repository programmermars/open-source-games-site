/* Runs before paint: apply the saved language and theme so the page does not flash. */
(function () {
  var r = document.documentElement, lang = null, theme = null;
  try {
    lang = localStorage.getItem("osg-lang");
    theme = localStorage.getItem("osg-theme");
  } catch (e) {}
  if (lang !== "zh" && lang !== "en") {
    var nav = (navigator.languages && navigator.languages[0]) || navigator.language || "";
    lang = /^zh/i.test(nav) ? "zh" : "en";
  }
  r.lang = lang === "en" ? "en" : "zh-CN";
  if (theme === "light" || theme === "dark") r.setAttribute("data-theme", theme);
})();
