from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, ProfileForm
from django.http import JsonResponse
from django.db.models import F


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            user.town = request.POST.get('t_address')
            user.building = request.POST.get('b_address')
            user.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

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