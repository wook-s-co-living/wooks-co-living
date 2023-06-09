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

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields["title"].widget.attrs["class"] = "cmty--form"
      self.fields["category"].widget.attrs["class"] = "cmty--form"
      self.fields["category"].widget.attrs["style"] = "width:100px"
      self.fields["title"].widget.attrs["placeholder"] = "제목"
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]