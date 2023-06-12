from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from taggit.models import Tag
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
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
    all_posts = Post.objects.all()
    categories = Post.objects.values_list('category', flat=True).distinct()

    category = request.GET.get('category')
    q = request.GET.get('q')
    tag = request.GET.get('tag')
    sort = request.GET.get('sort')

    if category and category != 'null':
        posts = Post.objects.filter(category=category).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct()
        
    if tag and tag != 'null':
        posts = posts.filter(tags__name=tag)

    if sort:
        posts = index_sort(sort, posts)
    else:
        posts = posts.order_by('-pk')

    top_writers = get_user_model().objects.exclude(Q(is_superuser=True) | Q(groups__name='admin') | Q(user_permissions__codename='admin')).order_by('-score')[:5]

    weekly_best_posts = Post.objects.annotate(like_count=Count('like_users')).order_by('-like_users')[:5]

    # Get the tags related to the filtered posts
    filtered_tags = Tag.objects.filter(post__in=all_posts).annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:10]

    context = {
        'categories': categories,
        'posts': posts,
        'filtered_tags': filtered_tags,
        'category': category,
        'all_posts': all_posts,
        'top_writers': top_writers,
        'weekly_best_posts': weekly_best_posts,
    }
    return render(request, 'communities/index.html', context)

@maum_limit
@login_required
def index_sort(o, queryset):
    if o == '최신순':
        return queryset.order_by('-pk')
    elif o == '추천순':
        return queryset.annotate(likes_diff=Count('like_users') - Count('dislike_users')).order_by('-likes_diff')
    elif o == '댓글순':
        return queryset.annotate(comment_count=Count('comments')).order_by('-comment_count')
    elif o == '스크랩순':
        return queryset.annotate(scrape_count=Count('scrape_users')).order_by('-scrape_count')
    elif o == '조회순':
        return queryset.order_by('-views')

@maum_limit
@login_required
def category(request, category):
    posts = Post.objects.filter(category=category).order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'communities/category.html')

@maum_limit
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
            request.user.score += 5
            request.user.save()
            return redirect('communities:detail', post.pk)
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form,
    }
    return render(request, 'communities/create.html', context)

@maum_limit
@login_required
def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = post.comments.filter(parent_comment=None)
    comment_form = CommentForm()

    comment_pk = request.session.pop('comment_pk', None)

    if comment_pk:
        comment = Comment.objects.get(pk=comment_pk)
        comment_section_id = f'comment-{comment.pk}'
    else:
        comment = None
        comment_section_id = None

    if not request.session.get("post_viewed_{}".format(post_pk)):
        post.views += 1
        post.save()
        request.session["post_viewed_{}".format(post_pk)] = True
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'comment': comment,
        'comment_section_id': comment_section_id,
        'likes_count': post.like_users.count()-post.dislike_users.count(),
        'KAKAO_JS_KEY': KAKAO_JS_KEY,
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

@maum_limit
@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if post.user == request.user:
        post.delete()
        request.user.score -= 5
        request.user.save()
    return redirect('communities:index')

@maum_limit
@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == "POST":
        post.tags.clear()
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

@maum_limit
@login_required
def scrapes(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if post.user == request.user:
        error_message = "자신의 글은 스크랩할 수 없습니다."
        return JsonResponse({"error": error_message})
    
    if post.scrape_users.filter(pk=request.user.pk).exists():
        post.scrape_users.remove(request.user)
        is_scraped = False
    else:
        post.scrape_users.add(request.user)
        is_scraped = True
    
    context = {
        "is_scraped": is_scraped,
    }

    return JsonResponse(context)

@maum_limit
@login_required
def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    like_value = request.POST.get("like_value")

    if post.user == request.user:
        error_message = "자신의 글은 추천할 수 없습니다."
        return JsonResponse({"error": error_message})

    if like_value == "like":
        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
            is_liked = False
            is_disliked = False

        elif post.dislike_users.filter(pk=request.user.pk).exists():
            post.dislike_users.remove(request.user)
            post.like_users.add(request.user)
            is_liked = True
            is_disliked = False

        else:
            post.like_users.add(request.user)
            is_liked = True
            is_disliked = False

    else:
        if post.dislike_users.filter(pk=request.user.pk).exists():
            post.dislike_users.remove(request.user)
            is_liked = False
            is_disliked = False

        elif post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
            post.dislike_users.add(request.user)
            is_liked = False
            is_disliked = True

        else:
            post.dislike_users.add(request.user)
            is_liked = False
            is_disliked = True

    context = {
        "is_liked": is_liked,
        "is_disliked": is_disliked,
        "post_like": post.like_users.count()-post.dislike_users.count()
    }

    return JsonResponse(context)

@maum_limit
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
                parent_comment = Comment.objects.get(pk=parent_pk)
                comment.parent_comment = parent_comment
                comment.depth = parent_comment.depth + 10
                if comment.depth > 50:
                    comment.depth = 10
            comment.save()
            request.user.score += 1
            request.user.save()
            request.session['comment_pk'] = comment.pk

            return redirect('communities:detail', post.pk)

@maum_limit
@login_required
def comment_update(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        comment_update_form = CommentForm(request.POST, instance=comment)
        if comment_update_form.is_valid():
            comment_update_form.save()
            context = {'commentContent': request.POST.get('comment-content')}
            return JsonResponse(context)
        else:
            print(comment_update_form.errors)

            
@maum_limit              
@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.user == comment.user:
        comment.delete()
        request.user.score -= 1
        request.user.save()

    post = Post.objects.get(pk=post_pk)
    comments = post.comments.filter(parent_comment=None)
    first_comment = comments.first()

    request.session['comment_pk'] = first_comment.pk

    return redirect('communities:detail', post_pk)

@maum_limit
@login_required
def comment_likes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    like_value = request.POST.get("like_value")

    if comment.user == request.user:
        error_message = "자신의 댓글은 추천할 수 없습니다."
        return JsonResponse({"error": error_message})

    if like_value == "like":
        if comment.like_users.filter(pk=request.user.pk).exists():
            comment.like_users.remove(request.user)
            is_liked = False
            is_disliked = False

        elif comment.dislike_users.filter(pk=request.user.pk).exists():
            comment.dislike_users.remove(request.user)
            comment.like_users.add(request.user)
            is_liked = True
            is_disliked = False

        else:
            comment.like_users.add(request.user)
            is_liked = True
            is_disliked = False

@maum_limit
@login_required
def comment_dislikes(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user in comment.dislike_users.all():
        comment.dislike_users.remove(request.user)
        comment_is_disliked = False
    else:
        if comment.dislike_users.filter(pk=request.user.pk).exists():
            comment.dislike_users.remove(request.user)
            is_liked = False
            is_disliked = False

        elif comment.like_users.filter(pk=request.user.pk).exists():
            comment.like_users.remove(request.user)
            comment.dislike_users.add(request.user)
            is_liked = False
            is_disliked = True

        else:
            comment.dislike_users.add(request.user)
            is_liked = False
            is_disliked = True

    context = {
        "is_liked": is_liked,
        "is_disliked": is_disliked,
        "comment_like": comment.like_users.count()-comment.dislike_users.count()
    }
    return JsonResponse(context)