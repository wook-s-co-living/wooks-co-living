# chat/views.py
from django.shortcuts import render, redirect
from .models import Chatroom
from django.db.models import Q
from accounts.models import User
from django.templatetags.static import static
from django.contrib import messages


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

@maum_limit
def index(request):
    chatrooms = Chatroom.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    sorted_chatrooms = sorted(chatrooms, key=lambda x: x.get_latest_message().created_at if x.get_latest_message() else x.created_at, reverse=True)
    context = {
        'chatrooms' : sorted_chatrooms,
    }
    return render(request, "chats/index.html", context)

@maum_limit
def room(request, first_name):
    user_name = User.objects.get(first_name=first_name).username
    user2 = User.objects.get(first_name=first_name)
    user2_image_url = user2.image.url if user2.image else static('image/noimage.png')
    try:
        room = Chatroom.objects.get(user1=request.user, user2=User.objects.get(username=user_name))
    except Chatroom.DoesNotExist:
        try:
            room = Chatroom.objects.get(user1=User.objects.get(username=user_name), user2=request.user)
        except Chatroom.DoesNotExist:
            room = Chatroom.objects.create(user1=request.user, user2=User.objects.get(username=user_name))

    room_name = room.pk
    messages = room.message_set.all()
    retriever = user_name
    retriever_name = User.objects.get(username=user_name).first_name

    context = {
        'room_name': room_name,
        'messages': messages,
        'retriever': retriever,
        'retriever_name': retriever_name,
        'user2' : user2,
        'user2_image_url': user2_image_url,
    }

    return render(request, "chats/room.html", context)


