from django.urls import path
from . import views

app_name="markets"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:market_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:market_pk>/update/', views.update, name='update'),
    path('<int:market_pk>/delete/', views.delete, name='delete'),
    path('<int:market_pk>/likes/', views.likes, name='likes'),
]
