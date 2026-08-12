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

    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/logout/", views.admin_logout, name="admin_logout"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),

    path("admin/article/new/", views.admin_article_form, name="admin_article_new"),
    path("admin/article/<int:pk>/edit/", views.admin_article_form, name="admin_article_edit"),
    path("admin/article/<int:pk>/delete/", views.admin_article_delete, name="admin_article_delete"),

    path("admin/thought/new/", views.admin_thought_form, name="admin_thought_new"),
    path("admin/thought/<int:pk>/edit/", views.admin_thought_form, name="admin_thought_edit"),
    path("admin/thought/<int:pk>/delete/", views.admin_thought_delete, name="admin_thought_delete"),

    path("admin/feed/new/", views.admin_feedpost_form, name="admin_feedpost_new"),
    path("admin/feed/<int:pk>/edit/", views.admin_feedpost_form, name="admin_feedpost_edit"),
    path("admin/feed/<int:pk>/delete/", views.admin_feedpost_delete, name="admin_feedpost_delete"),
]