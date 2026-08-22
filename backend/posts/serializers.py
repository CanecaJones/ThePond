from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post, Like, Repost


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    liked_by_me = serializers.SerializerMethodField()
    reposted_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "author", "content",
            "image", "video", "audio", "link",
            "created_at",
            "likes_count", "reposts_count", "liked_by_me", "reposted_by_me",
        ]
        read_only_fields = ["id", "author", "created_at"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_reposts_count(self, obj):
        return obj.reposts.count()

    def _current_user(self):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user
        return None

    def get_liked_by_me(self, obj):
        user = self._current_user()
        return user is not None and obj.likes.filter(user=user).exists()

    def get_reposted_by_me(self, obj):
        user = self._current_user()
        return user is not None and obj.reposts.filter(user=user).exists()

    def validate(self, data):
        if not data.get("content") and not any([
            data.get("image"), data.get("video"),
            data.get("audio"), data.get("link")
        ]):
            raise serializers.ValidationError(
                "O post precisa ter texto, mídia ou link."
            )
        return data