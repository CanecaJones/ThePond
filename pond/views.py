from django.shortcuts import render


def home(request):
    return render(request, "pond/home.html", {"active": "home"})


def articles(request):
    return render(request, "pond/articles.html", {"active": "articles"})


def article_detail(request, slug):
    return render(request, "pond/article_detail.html", {"active": "articles", "slug": slug})


def thoughts(request):
    return render(request, "pond/thoughts.html", {"active": "thoughts"})


def feed(request):
    return render(request, "pond/feed.html", {"active": "feed"})


def about(request):
    return render(request, "pond/about.html", {"active": "about"})