# chat/views.py
from django.shortcuts import render, redirect
from .models import Chatroom, Message
from django.db.models import Q
from accounts.models import User
from django.templatetags.static import static
from django.contrib import messages
from django.http import JsonResponse
import json


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
    
    for chatroom in chatrooms:
        chatroom.unchecked_message_count = chatroom.message_set.filter(retriever=request.user, is_checked=False).count()

    sorted_chatrooms = sorted(chatrooms, key=lambda x: x.get_latest_message().created_at if x.get_latest_message() else x.created_at, reverse=True)

    context = {
        'chatrooms': sorted_chatrooms,
        'requestUser': request.user,
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

    if(Chatroom.objects.filter(user1=request.user, user2=user2).first()):
        chatroom = Chatroom.objects.get(user1=request.user, user2=user2)
    else:
        chatroom = Chatroom.objects.get(user1=user2, user2=request.user)
    messages2 = Message.objects.filter(retriever=request.user, chatroom=chatroom)
    messages2.update(is_checked=True) # 

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


def update_latest_message(request):

    if request.method == 'POST':
        # AJAX 요청에서 데이터 추출
        dataset = json.loads(request.body.decode('utf-8'))
        print(dataset)
        # 상대방(sender)과 나(retriever)에 대한 정보 추출
        retriever = dataset['retriever']
        sender = dataset['sender']

        sender = User.objects.get(username=sender)
        retriever = User.objects.get(username=retriever)

        # 가장 최근의 메시지를 가져오는 로직
        latest_message = Message.objects.filter(
            sender=sender,
            retriever=retriever
        ).latest('created_at')

        # is_checked 필드를 1로 업데이트
        latest_message.is_checked = True
        latest_message.save()

        # 변경 완료 후 응답 반환
        response = {
            'message': 'Latest message updated successfully.'
        }
        return JsonResponse(response)
    
def delete(request, first_name):
    user = User.objects.get(first_name=first_name)

    if(Chatroom.objects.filter(user1=request.user, user2=user).first()):
        chatroom = Chatroom.objects.get(user1=request.user, user2=user)
    else:
        chatroom = Chatroom.objects.get(user1=user, user2=request.user)
    print('=================')
    print(chatroom)
    chatroom.delete()
    return redirect('chats:index')