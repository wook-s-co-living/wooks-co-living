from django import forms
from .models import Post, Comment
from taggit.models import Tag
from django.db.models import Count


class PostForm(forms.ModelForm):
    title = forms.CharField(label="")
    category = forms.CharField(label="")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ""
        
        
        # Get the available category choices from the database
        category_choices = list(Post.objects.exclude(category__isnull=True).exclude(category='').values_list('category', 'category'))
        
        # Get the popular tags and add their names to the category_choices list
        popular_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).filter(num_times__gt=5)
        for tag in popular_tags:
            category_choices.append((tag.name, tag.name))
        
        # Add a blank option at the beginning of the category_choices list
        category_choices.insert(0, ('', ''))
        arr = []
        for val in category_choices:
            if val not in arr:
                arr.append(val)
        
        category_choices = arr
        
        self.fields['category'] = forms.ChoiceField(choices=category_choices, required=False, label="")

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