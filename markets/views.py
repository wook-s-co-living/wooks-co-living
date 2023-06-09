from django.shortcuts import render, redirect
from .models import Post, Postimage
from .forms import PostForm, PostImageForm, DeleteImageForm
from django.db.models import Q
from chats.models import Chatroom
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import os
from dotenv import load_dotenv
load_dotenv()
KAKAO_JS_KEY = os.getenv('KAKAO_JS_KEY')
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')


def maum_limit(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.maum != 100:
                return view_func(request, *args, **kwargs)
            else:
                message = '신고 누적 5회차 이상으로 서비스 이용이 중지 되었습니다.\\n혼거동락팀에게 문의하세요.'
                messages.error(request, message)
                return redirect('index')
        else:
            return redirect('accounts:login')
    return wrapper

# Create your views here.

@maum_limit
@login_required
def index(request):
    dis = request.GET.get('dis')
    category = request.GET.get('category')
    q = request.GET.get('q')

    if dis == 'town':
        posts = Post.objects.filter(user__town=request.user.town)
    else:
        posts = Post.objects.filter(user__building=request.user.building)

    if category == 'used':
        posts = posts.filter(price__gt=0)
    elif category == 'free':
        posts = posts.filter(price=0)
    
    if q:
        posts = posts.filter(title__icontains=q)

    posts = posts.order_by('-pk')

    context = {'posts': posts}
    return render(request, 'markets/index.html', context)

@maum_limit
@login_required
def detail(request, market_pk):
    post = Post.objects.get(pk=market_pk)

    user_posts = post.user.user_markets_posts.order_by('-pk').exclude(pk=market_pk)[:6]

    post_user =  Post.objects.get(pk=market_pk).user

    chatrooms_length = Chatroom.objects.filter(Q(user1=post_user) | Q(user2=post_user)).count()

    if not request.session.get("post_viewed_{}".format(market_pk)):
        post.views += 1
        post.save()
        request.session["post_viewed_{}".format(market_pk)] = True
    
    post_form = PostForm(instance=post)

    context = {'post': post, 'user_posts': user_posts, 'KAKAO_JS_KEY': KAKAO_JS_KEY, 'chatrooms_length': chatrooms_length, 'post_form': post_form,}
    return render(request, 'markets/detail.html', context)

@maum_limit
@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('image_first')

        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.user = request.user
            form.save()
            for i in files:
                Postimage.objects.create(image_first=i, post=form)
            return redirect('markets:detail', form.pk)
        else:
            print(post_form.errors)
    else:
        post_form = PostForm()
        postimage_form = PostImageForm()

    context = {'post_form': post_form, 'postimage_form': postimage_form}
    return render(request, 'markets/create.html', context)

@maum_limit
@login_required
def update(request, market_pk):
    post = Post.objects.get(pk=market_pk)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        delete_ids = request.POST.getlist('delete_images')
        delete_form = DeleteImageForm(post=post, data=request.POST)
        files = request.FILES.getlist('image_first')

        if post_form.is_valid() and delete_form.is_valid():
            form = post_form.save()
            form.postimages.filter(pk__in=delete_ids).delete()
            for i in files:
                Postimage.objects.create(image_first=i, post=form)
            return redirect('markets:detail', form.pk)
        else:
            print(post_form.errors)

    else:
        post_form = PostForm(instance=post)
        delete_form = DeleteImageForm(post=post)
    if post.postimages.exists():
        postimage_form = PostImageForm(instance=post.postimages.first())
    else:
        postimage_form = PostImageForm()
    context = {
        'post': post,
        'post_form': post_form,
        'delete_form': delete_form,
        'postimage_form': postimage_form,
    }
    return render(request, 'markets/update.html', context)

@maum_limit
@login_required
def delete(request, market_pk):
    post = Post.objects.get(pk=market_pk)
    if request.user == post.user:
        post.delete()
    return redirect('markets:index')

@maum_limit
@login_required
def likes(request, market_pk):
    post = Post.objects.get(pk=market_pk)

    if post.user == request.user:
        error_message = "자신의 글은 관심글로 등록할 수 없습니다."
        return JsonResponse({'error': error_message})

    if request.user != post.user:
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
            is_liked = False
        else:
            post.like_users.add(request.user)
            is_liked = True

    context = {'is_liked': is_liked}
    return JsonResponse(context)


def update_sale_status(request, market_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=market_pk)
        post.sale_status = request.POST.get('sale_status')
        post.save()
    return redirect('markets:detail', market_pk)