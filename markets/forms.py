from django import forms
from .models import Post, Postimage
import os
from django.conf import settings

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'price',)

class PostImageForm(forms.ModelForm):
    class Meta:
        model = Postimage
        fields = ('image_first',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image_first'].widget.attrs['multiple'] = True

class DeleteImageForm(forms.Form):
    delete_images = forms.MultipleChoiceField(
        label='삭제할 이미지 선택',
        required = False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]
    )

    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_images'].choices = [
            (image.pk, image.image.name) for image in Postimage.objects.filter(post=post)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = Postimage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()