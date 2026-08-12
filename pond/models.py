from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class BaseTextContent(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField(help_text="Markdown")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"({self.pk})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "post"
            slug = base
            i = 1
            model = self.__class__
            while model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        words = len(self.body.split())
        minutes = max(1, round(words / 200))
        return minutes


class Article(BaseTextContent):
    cover_image = models.ImageField(upload_to="articles/", blank=True, null=True)

    class Meta(BaseTextContent.Meta):
        verbose_name = "Article"
        verbose_name_plural = "Articles"


class Thought(BaseTextContent):
    class Meta(BaseTextContent.Meta):
        verbose_name = "Thought"
        verbose_name_plural = "Thoughts"


class FeedPost(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Feed post"
        verbose_name_plural = "Feed posts"

    def __str__(self):
        return self.text[:50]


class FeedImage(models.Model):
    post = models.ForeignKey(FeedPost, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="feed/")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image for {self.post_id}"