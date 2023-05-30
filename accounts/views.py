from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash,get_user_model,login as auth_login, logout as auth_logout
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, ProfileForm
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from .models import User


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            # 닉네임 중복 제외
            first_name = form.cleaned_data.get('first_name')
            if User.objects.filter(first_name=first_name).exists():
              return redirect('accounts:signup')
            
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.address = request.POST.get('address')
            user.town = request.POST.get('t_address')
            user.building = request.POST.get('b_address')
            user.save()

            # 이메일 인증
            token = urlsafe_base64_encode(force_bytes(user.pk))
            user.activation_token = token
            user.save()

            current_site = get_current_site(request)
            mail_subject = '회원가입 인증 이메일'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': token,
                'activate_url' : f'http://127.0.0.1:8000/accounts/activate/{token}',
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# 이메일 인증 처리
def activate(request, token):
    try:
        uid = force_text(urlsafe_base64_decode(token))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.activation_token = None  # 토큰 삭제
        user.save()
        return redirect('accounts:login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # 인증 실패 처리
        return render(request, 'account/activation_error.html')
    
# 닉네임 중복확인
def check(request):
    first_name = request.GET.get('first_name')
    print(first_name)
    if User.objects.filter(first_name=first_name).exists():
        response_data = {'duplicate': True}
    else:
        response_data = {'duplicate': False}
    return JsonResponse(response_data)

# 아이디 중복확인 체크
def id_overlap_check(request):
    username = request.GET.get('username')
    try:
        # 중복 검사 실패
        user = User.objects.get(username=username)
    except:
        # 중복 검사 성공
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"
    context = {'overlap': overlap}
    return JsonResponse(context)

# 이메일 중복확인 체크
def email_overlap_check(request):
    email = request.GET.get('email')
    try:
        user = User.objects.get(email=email)
    except:
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"
    context = {'overlap': overlap}
    return JsonResponse(context)  

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            prev_url = request.session.get('prev_url')
            if prev_url:          
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('index')
        return redirect('accounts:login')
    else:
        form = CustomAuthenticationForm()
        request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')
    
@login_required
def delete(request):
    request.user.delete()
    return redirect('index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            user.town = request.POST.get('t_address')
            user.building = request.POST.get('b_address')
            user.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

    
@login_required
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile',request.user.username)
    else:
        form = ProfileForm(instance=person)
    context = {
        'person': person,
        'followings': person.followings.all(),
        'followers': person.followers.all(),
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)

    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', person.username)

@login_required
def followers_list(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    followers = person.followers.all()
    context = {
        'followers': followers,
        }
    return render(request, 'accounts/followers_list.html', context)

@login_required
def user_likes(request, username):
  User = get_user_model()
  person = User.objects.get(username=username)
  if request.user in person.likes.all():
      person.likes.remove(request.user)
      u_is_liked = False
  else:
      person.likes.add(request.user)
      u_is_liked = True
  person.update_maum()
  context = {
      'u_is_liked': u_is_liked,
      'user_likes_count': person.likes.count(),
      'u_is_disliked': request.user in person.dislikes.all(),
      'user_dislikes_count': person.dislikes.count(),
      'maum': person.maum,
  }
  return JsonResponse(context)

@login_required
def user_dislikes(request, username):
  User = get_user_model()
  person = User.objects.get(username=username)
  if request.user in person.dislikes.all():
      person.dislikes.remove(request.user)
      u_is_disliked = False
  else:
      person.dislikes.add(request.user)
      u_is_disliked = True
  person.update_maum()
  context = {
      'u_is_disliked': u_is_disliked,
      'user_dislikes_count': person.dislikes.count(),
      'u_is_liked': request.user in person.likes.all(),
      'user_likes_count': person.likes.count(),
      'maum': person.maum,
  }
  return JsonResponse(context)


# 비밀번호 재설정

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = get_user_model().objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = '[혼거동락] 비밀번호 재설정'
					email_template_name = "accounts/password_reset_email.txt"
					c = {
						"email": user.email,
						'domain': 'http://127.0.0.1:8000',
						'site_name': '혼거동락',
						"uid": urlsafe_base64_encode(force_bytes(user.pk)),
						"user": user,
						'token': default_token_generator.make_token(user),
						# 'protocol': settings.PROTOCOL,
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, '혼거동락 <jeongsodam26@gmail.com>' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("/accounts/password_reset_done/")
	password_reset_form = PasswordResetForm()
	return render(
		request=request,
		template_name='accounts/password_reset.html',
		context={'password_reset_form': password_reset_form})