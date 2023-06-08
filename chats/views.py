# chat/views.py
from django.shortcuts import render
from .models import Chatroom
from django.db.models import Q
from accounts.models import User
def index(request):
    chatrooms = Chatroom.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    sorted_chatrooms = sorted(chatrooms, key=lambda x: x.get_latest_message().created_at, reverse=True)
    context = {
        'chatrooms' : sorted_chatrooms,
    }
    return render(request, "chats/index.html", context)


def room(request, first_name):

    user_name = User.objects.get(first_name=first_name).username
    user2 = User.objects.get(first_name=first_name)
    user2_image_url = user2.image.url if user2.image else None

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
