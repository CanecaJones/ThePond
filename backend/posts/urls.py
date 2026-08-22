from django.urls import path
from .views import PostListCreateView, FeedView, LikeToggleView, RepostToggleView, UserPostsView

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("<int:post_id>/like/", LikeToggleView.as_view(), name="post-like"),
    path("<int:post_id>/repost/", RepostToggleView.as_view(), name="post-repost"),
    path("user/<str:handle>/", UserPostsView.as_view(), name="user-posts"),
]