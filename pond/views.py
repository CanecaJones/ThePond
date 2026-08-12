from django.shortcuts import render, get_object_or_404
from .models import Article, Thought, FeedPost


def home(request):
    recent_feed = FeedPost.published.all()[:4]
    return render(request, "pond/home.html", {"active": "home", "recent_feed": recent_feed})


def articles(request):
    items = Article.published.all()
    return render(request, "pond/articles.html", {"active": "articles", "items": items})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status="published")
    return render(request, "pond/article_detail.html", {"active": "articles", "article": article})


def thoughts(request):
    items = Thought.published.all()
    return render(request, "pond/thoughts.html", {"active": "thoughts", "items": items})


def feed(request):
    posts = FeedPost.published.all().prefetch_related("images")
    return render(request, "pond/feed.html", {"active": "feed", "posts": posts})


def about(request):
    return render(request, "pond/about.html", {"active": "about"})


def custom_404(request, exception):
    return render(request, "pond/404.html", {}, status=404)