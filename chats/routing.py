# chat/routing.py
from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path('ws/login/', consumers.LoginConsumer.as_asgi()),
    path('ws/alarm/', consumers.AlarmConsumer.as_asgi()),
    path('ws/index/', consumers.IndexConsumer.as_asgi()),
    
]