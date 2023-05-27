from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    once_datetime = forms.DateTimeField(
        widget = forms.DateTimeInput(
            attrs = {
                'type': 'datetime-local',
            }
        ),
        required = False,
    )
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "many_datetime",
            "once_datetime",
            "limit",
            "detail_address",
            "price",
            "image_first",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]