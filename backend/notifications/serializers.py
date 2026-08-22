from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    post_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "actor", "verb", "post_id", "read", "created_at"]

    def get_post_id(self, obj):
        return obj.post_id