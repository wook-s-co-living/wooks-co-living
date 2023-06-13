from django.urls import path
from . import views

app_name='moims'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:moim_pk>/', views.detail, name='detail'),
    path('<int:moim_pk>/update/', views.update, name='update'),
    path('<int:moim_pk>/delete/', views.delete, name='delete'),
    path('<int:moim_pk>/likes/', views.likes, name='likes'),
    path('<int:moim_pk>/joins/', views.joins, name='joins'),
    path('<int:moim_pk>/create/<int:parent_pk>/', views.comment_create, name='comment_create'),
    path('<int:moim_pk>/update/<int:comment_pk>/', views.comment_update, name='comment_update'),
    path('<int:moim_pk>/delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
    path('search/', views.search, name='search'),
    path('<int:moim_pk>/calendar/', views.calendar, name='calendar')
]