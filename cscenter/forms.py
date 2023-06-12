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

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields["title"].widget.attrs["class"] = "cs--form"
      self.fields["category"].widget.attrs["class"] = "cs--form"
      self.fields["category"].widget.attrs["style"] = "width:150px"
      self.fields["title"].widget.attrs["placeholder"] = "제목"