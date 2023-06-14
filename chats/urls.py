# chat/urls.py
from django.urls import path

from . import views

app_name="chats"
urlpatterns = [
    path("", views.index, name="index"),
    path("update_latest_message/", views.update_latest_message),
    path("get_chatroom_data/<int:chatroom_id>/", views.get_chatroom_data),
    path("<str:first_name>/", views.room, name="room"),
]