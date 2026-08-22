from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView, FollowToggleView, PublicProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("follow/<str:handle>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("profile/<str:handle>/", PublicProfileView.as_view(), name="public-profile"),
]