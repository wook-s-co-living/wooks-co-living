from django import forms
from .models import Post, Comment
from taggit.models import Tag
from django.db.models import Count


class PostForm(forms.ModelForm):
    category = forms.ChoiceField(label='카테고리', label_suffix='', choices=Post.category_Choices)
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]