(function () {
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;

  function apply(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    btn.textContent = theme === "light" ? "☀" : "☾";
  }

  btn.addEventListener("click", function () {
    var current = document.documentElement.getAttribute("data-theme") || "dark";
    var next = current === "dark" ? "light" : "dark";
    localStorage.setItem("pond-theme", next);
    apply(next);
  });

  apply(localStorage.getItem("pond-theme") || "dark");
})();