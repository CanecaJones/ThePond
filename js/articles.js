async function loadArticles() {

    const response = await fetch("data/articles.json");

    const articles = await response.json();

    const container = document.getElementById("articles");

    // Limpa a lista
    container.innerHTML = "";

    // Mais recente primeiro
    articles.reverse();

    // Cria cada artigo
    articles.forEach(article => {

        container.innerHTML += `

        <article class="post">

            <h2>

                <a href="article/${article.slug}.html">

                    ${article.title}

                </a>

            </h2>

            <p class="subtitle">

                ${article.subtitle}

            </p>

            <small>

                ${article.date}

            </small>

        </article>

        `;

    });

}

loadArticles();