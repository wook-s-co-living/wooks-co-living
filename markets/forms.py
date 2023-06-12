from django import forms
from .models import Post, Postimage
import os
from django.conf import settings
from django.core.validators import MinValueValidator
from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'moims/custom_clearable_file_input.html'


class PostForm(forms.ModelForm):
    title = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
    attrs={'class': 'market--form','placeholder' : '제목', 'autocomplete':'off'}))

    content = forms.CharField(label=False, label_suffix='', widget=forms.Textarea(
    attrs={'class': 'market--form','placeholder' : '상품에 대한 상세 설명을 작성 해주세요.', 'autocomplete':'off'}))
    
    price = forms.IntegerField(label='판매금액', widget=forms.NumberInput(
    attrs={'class': 'market--form'}),validators=[MinValueValidator(0)],initial=0)

    sale_status = forms.ChoiceField(label=False, choices=Post.sale_status_Choices, widget=forms.Select(
        attrs={'class': 'market--form'}
    ))

    class Meta:
        model = Post
        fields = ('title', 'content', 'price', 'sale_status',)

class PostImageForm(forms.ModelForm):
    image_first = forms.ImageField(
    label='상품 이미지',
    widget=CustomClearableFileInput(
        attrs={
            'multiple': True, 
            'class': 'market--form',
        }
    ),
)
        
    class Meta:
        model = Postimage
        fields = ('image_first',)

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
            (image.pk, image.image.url) for image in Postimage.objects.filter(post=post)
        ]

    def clean(self):
        cleaned_data = super().clean()
        delete_ids = cleaned_data.get('delete_images')
        if delete_ids:
            images = Postimage.objects.filter(pk__in=delete_ids)
            for image in images:
                os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
            images.delete()