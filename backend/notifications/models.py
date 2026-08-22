from django.conf import settings
from django.db import models


class Notification(models.Model):
    VERB_CHOICES = [
        ("follow", "Follow"),
        ("like", "Like"),
        ("repost", "Repost"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notifications",
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=10, choices=VERB_CHOICES)
    post = models.ForeignKey(
        "posts.Post",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"@{self.actor.handle} -> @{self.recipient.handle} ({self.verb})"