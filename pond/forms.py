from django import forms
from .models import Article, Thought, FeedPost, FeedImage


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "subtitle", "body", "cover_image", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"type": "text"}),
            "subtitle": forms.TextInput(attrs={"type": "text"}),
            "body": forms.Textarea(),
        }


class ThoughtForm(forms.ModelForm):
    class Meta:
        model = Thought
        fields = ["title", "subtitle", "body", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"type": "text"}),
            "subtitle": forms.TextInput(attrs={"type": "text"}),
            "body": forms.Textarea(),
        }


class FeedPostForm(forms.ModelForm):
    class Meta:
        model = FeedPost
        fields = ["text", "status"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 5}),
        }


FeedImageFormSet = forms.inlineformset_factory(
    FeedPost,
    FeedImage,
    fields=["image", "order"],
    extra=4,
    max_num=4,
    can_delete=True,
)