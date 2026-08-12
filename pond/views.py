from django.shortcuts import render, get_object_or_404
from .models import Article, Thought, FeedPost
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ArticleForm, ThoughtForm, FeedPostForm, FeedImageFormSet


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

def admin_login(request):
    if request.user.is_authenticated:
        return redirect("pond:admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("pond:admin_dashboard")
        messages.error(request, "Credenciais inválidas. Tenta de novo.")

    return render(request, "pond/admin/login.html", {})


def admin_logout(request):
    logout(request)
    return redirect("pond:admin_login")


@login_required(login_url="/admin/login/")
def admin_dashboard(request):
    context = {
        "articles": Article.objects.all()[:20],
        "thoughts": Thought.objects.all()[:20],
        "feed_posts": FeedPost.objects.all()[:20],
    }
    return render(request, "pond/admin/dashboard.html", context)

@login_required(login_url="/admin/login/")
def admin_article_form(request, pk=None):
    instance = get_object_or_404(Article, pk=pk) if pk else None
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Article salvo.")
            return redirect("pond:admin_dashboard")
    else:
        form = ArticleForm(instance=instance)
    return render(request, "pond/admin/article_form.html", {"form": form, "instance": instance})


@login_required(login_url="/admin/login/")
def admin_article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Article excluído.")
    return redirect("pond:admin_dashboard")

@login_required(login_url="/admin/login/")
def admin_thought_form(request, pk=None):
    instance = get_object_or_404(Thought, pk=pk) if pk else None
    if request.method == "POST":
        form = ThoughtForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Thought salvo.")
            return redirect("pond:admin_dashboard")
    else:
        form = ThoughtForm(instance=instance)
    return render(request, "pond/admin/thought_form.html", {"form": form, "instance": instance})


@login_required(login_url="/admin/login/")
def admin_thought_delete(request, pk):
    thought = get_object_or_404(Thought, pk=pk)
    if request.method == "POST":
        thought.delete()
        messages.success(request, "Thought excluído.")
    return redirect("pond:admin_dashboard")

@login_required(login_url="/admin/login/")
def admin_feedpost_form(request, pk=None):
    instance = get_object_or_404(FeedPost, pk=pk) if pk else None
    if request.method == "POST":
        form = FeedPostForm(request.POST, instance=instance)
        formset = FeedImageFormSet(request.POST, request.FILES, instance=instance if instance else FeedPost())
        if form.is_valid():
            post = form.save()
            formset.instance = post
            if formset.is_valid():
                formset.save()
                messages.success(request, "Post no feed salvo.")
                return redirect("pond:admin_dashboard")
    else:
        form = FeedPostForm(instance=instance)
        formset = FeedImageFormSet(instance=instance)
    return render(request, "pond/admin/feedpost_form.html", {"form": form, "formset": formset, "instance": instance})


@login_required(login_url="/admin/login/")
def admin_feedpost_delete(request, pk):
    post = get_object_or_404(FeedPost, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post excluído.")
    return redirect("pond:admin_dashboard")