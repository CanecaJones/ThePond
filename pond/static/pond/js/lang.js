(function () {
  var DICT = {
    pt: {
      "nav.feed": "Feed",
      "nav.articles": "Articles",
      "nav.thoughts": "Thoughts",
      "nav.about": "About",
      "home.subtitle": "Um blog. Sem funil de conversão, sem newsletter popup, sem 'inscreva-se'.",
      "home.recent": "Recentes no feed",
      "home.readmore": "ver mais →",
      "empty.feed": "Nada por aqui. Nem toda ideia vira post.",
      "empty.articles": "Nenhum artigo ainda. A ideia existe, o texto não.",
      "empty.thoughts": "Nenhum thought publicado. Os pensamentos estão, mas ainda desorganizados.",
      "empty.search": "Procurou e não achou. Bem-vindo ao meu código de 2019.",
      "loading": "Carregando...",
      "readtime": "min de leitura",
      "404.title": "404",
      "404.message": "Essa página não existe. Assim como testes unitários no meu primeiro projeto.",
      "404.back": "Voltar pra home",
      "footer.quote": "Debugging is twice as hard as writing the code in the first place.",
      "footer.webring": "Um webring pra quem ainda lê man page",
      "articles.title": "Articles",
      "articles.subtitle": "Textos longos. Leia sentado.",
      "thoughts.title": "Thoughts",
      "thoughts.subtitle": "Textos curtos, menos revisados, mais honestos.",
      "feed.title": "Feed",
      "feed.subtitle": "Tipo Twitter, mas sem o algoritmo tentando me deixar bravo.",
      "about.title": "About",
    },
    en: {
      "nav.feed": "Feed",
      "nav.articles": "Articles",
      "nav.thoughts": "Thoughts",
      "nav.about": "About",
      "home.subtitle": "A blog. No conversion funnel, no newsletter popup, no 'subscribe now'.",
      "home.recent": "Recent on the feed",
      "home.readmore": "read more →",
      "empty.feed": "Nothing here. Not every idea becomes a post.",
      "empty.articles": "No articles yet. The idea exists, the text doesn't.",
      "empty.thoughts": "No thoughts published. They're there, just unorganized.",
      "empty.search": "You searched and found nothing. Welcome to my 2019 codebase.",
      "loading": "Loading...",
      "readtime": "min read",
      "404.title": "404",
      "404.message": "This page doesn't exist. Much like the unit tests in my first project.",
      "404.back": "Back to home",
      "footer.quote": "Debugging is twice as hard as writing the code in the first place.",
      "footer.webring": "A webring for people who still read man pages",
      "articles.title": "Articles",
      "articles.subtitle": "Long-form. Sit down for these.",
      "thoughts.title": "Thoughts",
      "thoughts.subtitle": "Shorter pieces, less edited, more honest.",
      "feed.title": "Feed",
      "feed.subtitle": "Like Twitter, minus the algorithm trying to make me angry.",
      "about.title": "About",
    }
  };

  function applyLang(lang) {
    document.documentElement.setAttribute("lang", lang === "pt" ? "pt-BR" : "en");
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (DICT[lang] && DICT[lang][key]) {
        el.textContent = DICT[lang][key];
      }
    });
    var langBtn = document.getElementById("lang-btn");
    if (langBtn) langBtn.textContent = lang.toUpperCase() + " ▼";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var saved = localStorage.getItem("pond-lang") || "pt";
    applyLang(saved);

    var toggleBtn = document.getElementById("lang-btn");
    var menu = document.getElementById("lang-menu");
    if (toggleBtn && menu) {
      toggleBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        menu.classList.toggle("open");
      });
      document.addEventListener("click", function () {
        menu.classList.remove("open");
      });
      menu.querySelectorAll("button").forEach(function (b) {
        b.addEventListener("click", function () {
          localStorage.setItem("pond-lang", b.dataset.lang);
          applyLang(b.dataset.lang);
          menu.classList.remove("open");
        });
      });
    }
  });
})();