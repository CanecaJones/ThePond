from django.urls import path
from . import views

app_name = "pond"

urlpatterns = [
    path("", views.home, name="home"),
    path("articles", views.articles, name="articles"),
    path("article/<slug:slug>", views.article_detail, name="article_detail"),
    path("thoughts", views.thoughts, name="thoughts"),
    path("feed", views.feed, name="feed"),
    path("about", views.about, name="about"),
]