from django.urls import path
from .views import NotificationListView, UnreadCountView, MarkAllReadView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("unread-count/", UnreadCountView.as_view(), name="notification-unread-count"),
    path("mark-read/", MarkAllReadView.as_view(), name="notification-mark-read"),
]