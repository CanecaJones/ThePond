from django.contrib import admin
from .models import Article, Thought, FeedPost, FeedImage


class FeedImageInline(admin.TabularInline):
    model = FeedImage
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at", "reading_time")
    list_filter = ("status",)
    search_fields = ("title", "subtitle", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at", "reading_time")
    list_filter = ("status",)
    search_fields = ("title", "subtitle", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FeedPost)
class FeedPostAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status", "created_at")
    list_filter = ("status",)
    inlines = [FeedImageInline]