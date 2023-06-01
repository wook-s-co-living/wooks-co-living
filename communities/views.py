from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.db.models import Q, Count
from django.utils.html import escape
from django.views.generic import ListView, TemplateView
from taggit.models import Tag
from datetime import date, datetime, timedelta

# Create your views here.
class TagCloudTV(TemplateView):
    template_name = 'communities/index.html'


class TaggedObjectLV(ListView):
    template_name = 'communities/tag_with_post.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
    
def index(request):
    categories = Post.objects.values_list('category', flat=True).distinct()
    cate = request.GET.get('cate')
    if cate:
        posts = Post.objects.filter(category=cate).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    popular_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).filter(num_times__gt=5)
    context = {
        'posts': posts,
        'popular_tags': popular_tags,
        'categories': categories,
    }
    return render(request, 'communities/index.html', context)

def category(request, category):
    posts = Post.objects.filter(category=category).order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'communities/category.html')

@login_required
def create(request):
    if request.method == "POST":
        tags = request.POST.get('tag','').split(',')
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    post.tags.add(tag)
            post.save()
            return redirect('communities:detail', post.pk)
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form,
    }
    return render(request, 'communities/create.html', context)

def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    login_session = request.session.get('login_session', '')
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'login_session': login_session,
    }
    response = render(request, 'communities/detail.html', context)

    # 조회수 기능 (쿠키 사용)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitboard', '_')

    if f'_{post.pk}_' not in cookie_value:
        cookie_value += f'{post.pk}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        post.views += 1
        post.save()
    return response

def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.user == request.user:
        post.delete()
    return redirect('communities:index')

def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == "POST":
        tags = request.POST.get('tag','').split(',')
        update_form = PostForm(request.POST, instance=post)
        if update_form.is_valid():
            update = update_form.save()
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    update.tags.add(tag)
            update.save()
            return redirect('communities:detail', post.pk)
    else:
        update_form = PostForm(instance=post)
    context = {
        'post': post,
        'update_form': update_form,
    }
    return render(request, 'communities/update.html', context)

@login_required
def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked
    }
    # return redirect('communities:detail', post.pk)
    return JsonResponse(context)

@login_required
def dislikes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.dislike_users.all():
        post.dislike_users.remove(request.user)
        is_disliked = False
    else:
        post.dislike_users.add(request.user)
        is_disliked = True
    context = {
        'is_disliked': is_disliked
    }
    # return redirect('communities:detail', post.pk)
    return JsonResponse(context)

@login_required
def comment_create(request, post_pk, parent_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_pk != 0:
                comment.parent_comment = Comment.objects.get(pk=parent_pk)
            comment.save()
            return redirect('communities:detail', post.pk)

def comment_update(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        comment_update_form = CommentForm(request.POST, instance=comment)
        if comment_update_form.is_valid():
            comment_update_form.save()
            return redirect('communities:detail', post_pk)
        
def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('communities:detail', post_pk)

@login_required
def comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
        comment_is_liked = False
    else:
        comment.like_users.add(request.user)
        comment_is_liked = True
    context = {
        'comment_is_liked': comment_is_liked
    }
    return JsonResponse(context)

@login_required
def comment_dislikes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user in comment.dislike_users.all():
        comment.dislike_users.remove(request.user)
        comment_is_disliked = False
    else:
        comment.dislike_users.add(request.user)
        comment_is_disliked = True
    context = {
        'comment_is_disliked': comment_is_disliked
    }
    return JsonResponse(context)

def search(request):
    post_list = Post.objects.all()
    search_text = request.GET.get('search')
    search_list = []
    if search_text:
        search_list = post_list.filter(
            Q(title__icontains=search_text) |
            Q(content__icontains=search_text) |
            Q(user__username__icontains=search_text) |
            Q(tags__name__icontains=search_text) |
            Q(category__icontains=search_text)
        ).distinct()
    
        for search_item in search_list:
            search_item.title = mark_safe(search_item.title.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))
            search_item.content = mark_safe(search_item.content.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))
            search_item.user.username = mark_safe(search_item.user.username.replace(search_text, '<span style="color:red;">{}</span>'.format(escape(search_text))))

    context = {
        'search_list': search_list,
        'search_text': search_text,
    }
    return render(request,'communities/search.html', context)