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
CALENDAR_API_KEY = os.getenv('CALENDAR_API_KEY')
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import credentials
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def calendar(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    clndr(post)
    return redirect('moims:detail', moim_pk)

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
    category = request.GET.get('category')
    dis = request.GET.get('dis')    
    q = request.GET.get('q')
    
    if category == 'once':
        posts = Post.objects.filter(category=category,once_datetime__gte=timezone.now()).order_by('once_datetime')
    else:
        posts = Post.objects.filter(category='many').order_by('-pk')

    if dis == 'town':
        posts = posts.filter(user__town=request.user.town)
    else:
        posts = posts.filter(user__building=request.user.building)

    if q:
        posts = posts.filter(title__icontains=q)

    context = {'posts': posts,}

    return render(request, 'moims/many.html', context)

@maum_limit
@login_required
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
            post.join_users.add(request.user)
            return redirect('moims:detail', post.pk)
    else:
        post_form = PostForm()
    context = {
        'post_form': post_form
    }
    return render(request, 'moims/create.html', context)

def clndr(post):
    
    creds = None

    if os.path.exists('token.json'):
        print("1111111")
        creds = credentials.Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("222222")
            creds.refresh(Request())
        else:
            print("333333")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            print("444444")
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        once_datetime = post.once_datetime
        end_datetime = once_datetime + timedelta(hours=2)
        once_datetime_str = once_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')
        end_datetime_str = end_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')
        ev = {
            'summary': post.title,
            'location': post.address,
            'description': f"http://127.0.0.1:8000/moims/{post.pk}/",
            'start': {
                'dateTime': once_datetime_str,
                'timeZone': 'Asia/Seoul',
            },
            'end': {
                'dateTime': end_datetime_str,
                'timeZone': 'Asia/Seoul',
            },
            'attendees': [
                {'email': post.user.email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=ev).execute()
        
    except HttpError as error:
        print('An error occurred: %s' % error)

@maum_limit
@login_required
def detail(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    comments = post.comments.filter(parent_comment=None)
    comment_form = CommentForm()

    comment_pk = request.session.pop('comment_pk', None)

    if comment_pk:
        comment = Comment.objects.get(pk=comment_pk)
        comment_section_id = f'comment-{comment.pk}'
    else:
        comment = None
        comment_section_id = None

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'KAKAO_JS_KEY': KAKAO_JS_KEY,
        'comment': comment,
        'comment_section_id': comment_section_id,
    }
    return render(request, 'moims/detail.html', context)


@maum_limit
@login_required
def update(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.method == "POST":
        update_form = PostForm(request.POST, request.FILES, instance=post)
        if update_form.is_valid():
            post = update_form.save(commit=False)
            post.address = request.POST.get('address')
            post.town = request.POST.get('t_address')
            post.building = request.POST.get('b_address')
            post.save()
            return redirect('moims:detail', post.pk)
    else:
        update_form = PostForm(instance=post)
    context = {
        'post': post,
        'update_form': update_form,
    }
    return render(request, 'moims/update.html', context)

@maum_limit
@login_required
def delete(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    if request.user == post.user:
        post.delete()
    return redirect('moims:index')


@maum_limit
@login_required
def likes(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)

    if post.user == request.user:
        error_message = "자신의 모임은 관심모임으로 등록할 수 없습니다."
        return JsonResponse({'error': error_message})

    if request.user != post.user:
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
            is_liked = False
        else:
            post.like_users.add(request.user)
            is_liked = True
    context = {'is_liked': is_liked}
    return JsonResponse(context)

@maum_limit
@login_required
def joins(request, moim_pk):
    post = Post.objects.get(pk=moim_pk)
    print(request.GET.get('out'))
    if post.user == request.user:
        error_message = "자신의 모임은 참여할 수 없습니다."
        return JsonResponse({'error': error_message})
    elif post.limit == post.join_users.count() and request.GET.get('out') == 'null':
        error_message = "참여인원이 가득 찼습니다."
        return JsonResponse({'error': error_message})
    
    if request.user != post.user:
        if request.user in post.join_users.all():
            post.join_users.remove(request.user)
            is_joined = False
        else:
            post.join_users.add(request.user)
            is_joined = True

    context = {'is_joined': is_joined}
    return JsonResponse(context)

@maum_limit
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
                parent_comment = Comment.objects.get(pk=parent_pk)
                comment.parent_comment = parent_comment
                comment.depth = parent_comment.depth + 10
                if comment.depth > 50:
                    comment.depth = 10
            comment.save()
            request.session['comment_pk'] = comment.pk

            return redirect('moims:detail', moim_pk=moim_pk)
 
@maum_limit
@login_required
def comment_update(request, moim_pk, comment_pk):
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
def comment_delete(request, moim_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    if request.user == comment.user:
        comment.delete()

    post = Post.objects.get(pk=moim_pk)
    comments = post.comments.filter(parent_comment=None)
    first_comment = comments.first()

    request.session['comment_pk'] = first_comment.pk

    return redirect('moims:detail', moim_pk=moim_pk)

@maum_limit
@login_required
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