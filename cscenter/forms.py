from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    category = forms.ChoiceField(label='카테고리', label_suffix='', choices=Post.category_Choices)
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
        ]