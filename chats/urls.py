# chat/urls.py
from django.urls import path

from . import views

app_name="chats"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:first_name>/", views.room, name="room"),
]