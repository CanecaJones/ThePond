from django.conf import settings
from django.db import models
from .validators import validate_video_size


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.CharField(max_length=300, blank=True, default="")

    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
    video = models.FileField(
        upload_to="posts/videos/",
        blank=True,
        null=True,
        validators=[validate_video_size]
    )
    audio = models.FileField(upload_to="posts/audio/", blank=True, null=True)
    link = models.URLField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"@{self.author.handle}: {self.content[:30]}"

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="likes",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")


class Repost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reposts",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name="reposts",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")