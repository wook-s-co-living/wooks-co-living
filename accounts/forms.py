from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User, Reportimage
from django import forms
from django.forms.widgets import ClearableFileInput


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('username','password1', 'password2','email', 'last_name', 'first_name', 'gender', 'age', 'image_first',)
    
    gender_Choices = (('male','남성'),('female','여성'))
    age_Choices = (('10','20대 미만'),('20','20대'),('30','30대'),('40','40대'),('50','50대'),('60','60대 이상'))

    username = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '아이디', 'autocomplete':'off', 'style':'margin-bottom:0 !important;'}))
    password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '비밀번호','style':'margin-top:0.8rem !important;'}))
    password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '비밀번호 확인'}))
    last_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '이름', 'autocomplete':'off','style':'margin-top:0.8rem !important;'}))
    first_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '닉네임', 'autocomplete':'off', 'style':'margin-bottom:0 !important;'}))
    email = forms.EmailField(label=False, label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'signup--form','placeholder' : '이메일', 'autocomplete':'off', 'style':'margin-bottom:0 !important;'}))
    gender = forms.ChoiceField(label='성별', label_suffix='', choices=gender_Choices, widget=forms.Select(
        attrs={'class': 'signup--form'}))
    age = forms.ChoiceField(label='연령대', label_suffix='', choices=age_Choices, widget=forms.Select(
        attrs={'class': 'signup--form'}))

    image_first = forms.ImageField(
        required=False,
        label='프로필 이미지',
        widget=forms.ClearableFileInput(attrs={'class': 'signup--form'}),
    )

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'accounts/custom_clearable_file_input.html'

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'last_name', 'first_name', 'gender', 'age', 'image_first',)

    gender_Choices = (('male','남성'),('female','여성'))
    age_Choices = (('10','20대 미만'),('20','20대'),('30','30대'),('40','40대'),('50','50대'),('60','60대 이상'))
    last_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '이름', 'autocomplete':'off'}))
    first_name = forms.CharField(label=False, label_suffix='', widget=forms.TextInput(
        attrs={'class': 'signup--form','placeholder' : '닉네임', 'autocomplete':'off'}))
    email = forms.EmailField(label=False, label_suffix='', widget=forms.EmailInput(
        attrs={'class': 'signup--form','placeholder' : '이메일', 'autocomplete':'off'}))
    gender = forms.ChoiceField(label='성별', label_suffix='', choices=gender_Choices, widget=forms.Select(
        attrs={'class': 'signup--form'}))
    age = forms.ChoiceField(label='연령대', label_suffix='', choices=age_Choices, widget=forms.Select(
        attrs={'class': 'signup--form'}))

    image_first = forms.ImageField(
        required=False,
        label='프로필 이미지',
        widget=CustomClearableFileInput(attrs={'class': 'signup--form'}),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)
    old_password = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '기존 비밀번호'}))
    new_password1 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '새 비밀번호'}))
    new_password2 = forms.CharField(label=False, label_suffix='', widget=forms.PasswordInput(
        attrs={'class': 'signup--form','placeholder' : '새 비밀번호 확인'}))
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['introduce']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['introduce'].label = False

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'login--form ',
                'placeholder': '아이디',
                'style': 'border-bottom: none;border-top-left-radius: 0.375rem;border-top-right-radius: 0.375rem;',
            }
        )
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'login--form ',
                'placeholder': '비밀번호',
                'style': 'border-bottom-left-radius: 0.375rem;border-bottom-right-radius: 0.375rem;',
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.add_error('username', '가입되어있지 않은 ID입니다. 다시 확인해주세요.')
                return

            if not user.check_password(password):
                self.add_error('password', '비밀번호가 올바르지 않습니다. 다시 확인해주세요.')

        return self.cleaned_data
    
class ReportImageForm(forms.ModelForm):
    image_first = forms.ImageField(
    label='관련 이미지',
    required=False,
    widget=CustomClearableFileInput(
        attrs={
            'multiple': True, 
            'class': 'report--form',
        }
    ),
)
        
    class Meta:
        model = Reportimage
        fields = ('image_first',)