from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from accounts.models import User
import os
from dotenv import load_dotenv
load_dotenv()
KAKAO_JS_KEY = os.getenv('KAKAO_JS_KEY')
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.db.models import Q

# Create your views here.
def many(request):
    posts = Post.objects.filter(category = 'many').order_by('-created_at')
    # user_building = request.user.building
    # building_posts = Post.objects.filter(category='once', user__building = user_building).order_by('-created_at')
    # user_town = request.user.town
    # town_posts = Post.objects.filter(category='once', town = user_town).order_by('-created_at')
    context = {
        'posts': posts,
        'KAKAO_JS_KEY': KAKAO_JS_KEY,
    }
    return render(request, 'moims/many.html', context)

def once(request):
    posts = Post.objects.filter(category = 'once').order_by('-created_at')
    # user_building = request.user.building
    # building_posts = Post.objects.filter(category='once', user__building = user_building).order_by('-created_at')
    # user_town = request.user.town
    # town_posts = Post.objects.filter(category='once', town = user_town).order_by('-created_at')
    context = {
        'posts': posts,
        'KAKAO_JS_KEY': KAKAO_JS_KEY,
    }
    return render(request, 'moims/once.html', context)

def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.address = request.POST.get('address')
            post.town = request.POST.get('t_address')
            post.building = request.POST.get('b_address')
            post.save()
            return redirect('moims:detail', post.pk)
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form
    }
    return render(request, 'moims/create.html', context)

def detail(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'KAKAO_JS_KEY': KAKAO_JS_KEY,
    }
    return render(request, 'moims/detail.html', context)

def update(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.method == "POST":
        update_form = PostForm(request.POST, request.FILES, instance=post)
        if update_form.is_valid():
            post = update_form.save()
            return redirect('moims:detail', post.pk)
    else:
        update_form = PostForm(instance=post)
    context = {
        'post': post,
        'update_form': update_form,
    }
    return render(request, 'moims/update.html', context)

def delete(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.user == post.user:
        post.delete()
    return redirect('moims:many')

@login_required
def likes(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked
    }
    return JsonResponse(context)

@login_required
def joins(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.user in post.join_users.all():
        post.join_users.remove(request.user)
        is_joined = False
    else:
        post.join_users.add(request.user)
        is_joined = True
    context = {
        'is_joined': is_joined
    }
    return JsonResponse(context)

@login_required
def comment_create(request, moim_pk, parent_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_pk != 0:
                comment.parent_comment = Comment.objects.get(pk=parent_pk)
            comment.save()
            # 비동기
            return JsonResponse()
            # 생성 테스트용 (비동기 적용 X)
            # return redirect('moims:detail', post.pk)
    else:
        comment_form = CommentForm()
    context = {
        'comment_form': comment_form,
        'post': post,
    }
    return render(request, 'moims/detail.html', context)

@login_required
def comment_update(request, moim_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            jsonObject = json.loads(request.body)
            comment.content = jsonObject['content']
            comment.save()
    context = {

    }
    return JsonResponse(context)

@login_required
def comment_delete(request, moim_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('moims:detail', moim_pk=moim_pk)

def search(request):
    category = request.GET.get('category')
    cate = None
    if category == 'many':
        post_list = Post.objects.filter(category='many').order_by('-created_at')
        cate = 'many'
    elif category == 'once':
        post_list = Post.objects.filter(category='once').order_by('-created_at')
        cate = 'once'
    else:
        post_list = Post.objects.all()
    search_text = request.GET.get('search')
    search_list = []
    if search_text:
        search_list = post_list.filter(
            Q(title__icontains=search_text) |
            Q(content__icontains=search_text) |
            Q(address__icontains=search_text) |
            Q(town__icontains=search_text) |
            Q(detail_address__icontains=search_text)
        ).distinct()
    
        for search_item in search_list:
            search_item.title = mark_safe(search_item.title.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))
            search_item.content = mark_safe(search_item.content.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))
            search_item.address = mark_safe(search_item.address.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))
            search_item.town = mark_safe(search_item.town.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))
            search_item.detail_address = mark_safe(search_item.detail_address.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))

    context = {
        'search_list': search_list,
        'search_text': search_text,
        'cate': cate,
    }
    return render(request,'moims/search.html', context)