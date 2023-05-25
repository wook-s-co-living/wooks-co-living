from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill
from django import forms
from django.forms.widgets import ClearableFileInput


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('username','password1', 'password2','email', 'last_name', 'first_name', 'gender', 'age', 'image_first',)
    
    gender_Choices = (('male','남성'),('female','여성'))
    age_Choices = (('10','20대 미만'),('20','20대'),('30','30대'),('40','40대'),('50','50대'),('60','60대 이상'))

    username = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '아이디', 'autocomplete':'off'}))
    password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '비밀번호'}))
    password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '비밀번호 확인'}))
    last_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '이름', 'autocomplete':'off'}))
    first_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '닉네임', 'autocomplete':'off'}))
    email = forms.EmailField(label=False, label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'signup--form','placeholder' : '이메일', 'autocomplete':'off'}))
    gender = forms.ChoiceField(label='성별', label_suffix='', choices=gender_Choices, widget=forms.Select(
        attrs={'class': 'signup--form','style' : 'width: 50%;'}))
    age = forms.ChoiceField(label='연령대', label_suffix='', choices=age_Choices, widget=forms.Select(
        attrs={'class': 'signup--form','style' : 'width:50%;'}))

    image_first = forms.ImageField(
        required=False,
        label='프로필 이미지',
        widget=forms.ClearableFileInput(attrs={'class': 'signup--form','style' : 'margin-bottom:10px;'}),
    )

# class CustomClearableFileInput(ClearableFileInput):
#     template_name = 'posts/custom_clearable_file_input.html'

# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm):
#         model = get_user_model()
#         fields = ('last_name', 'image', 'email', 'is_owner', 'region',)
#     last_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
#         attrs={'class': 'form-box','placeholder' : '이름','style' : 'width:400px;'}))
    

#     email = forms.EmailField(label='이메일', label_suffix='', widget=forms.EmailInput(
#         attrs={'class': 'form-box','placeholder' : '이메일','style' : 'width:400px;'}))
#     image = ProcessedImageField(
#         required=False,
#         widget=CustomClearableFileInput(attrs={'class': 'form-box','style' : 'width:400px;'}),
#         label='프로필 이미지',
#         label_suffix='',
#         spec_id='image_size',
#     )
    
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.pop('password')
 

# class CustomPasswordChangeForm(PasswordChangeForm):
#     class Meta(UserChangeForm):
#         model = get_user_model()
#         fields = ('old_password', 'new_password1', 'new_password2',)
#     old_password = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
#         attrs={'class': 'form-box','placeholder' : '기존 비밀번호','style' : 'width:400px;'}))
#     new_password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
#         attrs={'class': 'form-box','placeholder' : '새 비밀번호','style' : 'width:400px;'}))
#     new_password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
#         attrs={'class': 'form-box','placeholder' : '새 비밀번호 확인','style' : 'width:400px;'}))
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs = {
                'class': 'login--form ',
                'placeholder' : '아이디',
                'style': 'border-bottom: none;border-top-left-radius: 0.375rem;border-top-right-radius: 0.375rem;',
            }
        )
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'login--form ',
                'placeholder' : '비밀번호',
                'style': 'border-bottom-left-radius: 0.375rem;border-bottom-right-radius: 0.375rem;',
            }
        )
    )
    

