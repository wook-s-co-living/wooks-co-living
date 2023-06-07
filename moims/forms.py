from django import forms
from .models import Post, Comment
from django.core.validators import MinValueValidator
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'moims/custom_clearable_file_input.html'

class PostForm(forms.ModelForm):
    title = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
    attrs={'class': 'moims--form','placeholder' : '모임 제목', 'autocomplete':'off'}))

    content = forms.CharField(label=False, label_suffix='', widget=forms.Textarea(
    attrs={'class': 'moims--form','placeholder' : '모임에 대한 상세 설명을 작성 해주세요.', 'autocomplete':'off'}))

    category = forms.ChoiceField(label='정기/당일', label_suffix='',choices=Post.category_Choices, widget=forms.Select(
    attrs={'class': 'moims--form'}))
    
    many_datetime = forms.CharField(label=False, label_suffix='', required = False, widget=forms.TextInput(
    attrs={'class': 'moims--form','placeholder' : '정기 모임 일자', 'autocomplete':'off'}))

    once_datetime = forms.DateTimeField(
        label='날짜',
        widget = forms.DateTimeInput(
            attrs = {
                'class': 'moims--form',
                'type': 'datetime-local',
            }
        ),
        required = False,
    )

    limit = forms.IntegerField(label='인원(명)', label_suffix='', widget=forms.NumberInput(
    attrs={'class': 'moims--form'}),validators=[MinValueValidator(1)],initial=1)

    price = forms.IntegerField(label='참가비(원)', label_suffix='', widget=forms.NumberInput(
    attrs={'class': 'moims--form'}),validators=[MinValueValidator(0)],initial=0)

    image_first = forms.ImageField(
    label='모임 대표 이미지',
    widget=CustomClearableFileInput(attrs={'class': 'moims--form'}),
    )

    kakao_url = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
    attrs={'class': 'moims--form','placeholder' : '카카오 오픈채팅방 주소', 'autocomplete':'off'}))

    detail_address = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
    attrs={'class': 'moims--form','placeholder' : '상세주소', 'autocomplete':'off'}))

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "many_datetime",
            "once_datetime",
            "limit",
            "kakao_url",
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