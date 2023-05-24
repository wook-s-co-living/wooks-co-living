from django.urls import path
from . import views

app_name='moims'
urlpatterns = [
    path('many/', views.many, name='many')
]