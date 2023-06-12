from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils.html import strip_tags
import requests, json

# Create your views here.
def index(request):
    if request.user.is_superuser == False:
        my_posts = Post.objects.filter(user=request.user)
    else:
        my_posts = Post.objects.filter(user__is_superuser=False)
    all_posts = Post.objects.filter(user__is_superuser=True)
    categories = Post.objects.values_list('category', flat=True).distinct()
    first_objects = []
    for category in categories:
        first_object = all_posts.filter(category=category).order_by('id').first()
        if first_object:
            first_objects.append(first_object)
    category = request.GET.get('category')
    posts = all_posts.none()

    if category:
        posts = all_posts.filter(category=category).order_by('-created_at')
        
    context = {
        'categories': categories,
        'posts': posts,
        'category': category,
        'all_posts': all_posts,
        'first_objects': first_objects,
        'my_posts': my_posts,
    }
    return render(request, 'cscenter/index.html', context)

def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            # 이메일 발송
            if request.user.is_superuser == False:
                text_content = strip_tags(post.content)
                subject = post.title
                message = f"Content: {text_content}\nUser email: {post.user.email}"
                from_email = 'hongeodonglag@gmail.com'
                recipient_list = ['hongeodonglag@gmail.com']
                send_mail(subject, message, from_email, recipient_list)
            return redirect('cscenter:detail', post.pk)
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form,
    }
    return render(request, 'cscenter/create.html', context)

def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    all_posts = Post.objects.filter(user__is_superuser=True)
    categories = Post.objects.values_list('category', flat=True).distinct()
    first_objects = []
    for category in categories:
        first_object = all_posts.filter(category=category).order_by('id').first()
        if first_object and first_object != post:
            first_objects.append(first_object)

    context = {
        'post': post,
        'first_objects': first_objects,
    }
    return render(request, 'cscenter/detail.html', context)

def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.user == request.user:
        post.delete()
    return redirect('cscenter:index')

def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == "POST":
        update_form = PostForm(request.POST, instance=post)
        if update_form.is_valid():
            update = update_form.save()
            return redirect('cscenter:detail', post.pk)
    else:
        update_form = PostForm(instance=post)
    context = {
        'post': post,
        'update_form': update_form,
    }
    return render(request, 'cscenter/update.html', context)