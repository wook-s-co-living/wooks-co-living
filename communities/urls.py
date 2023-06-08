from django.urls import path
from . import views

app_name="communities"
urlpatterns = [
    path('', views.index, name='index'),
    # path('<str:category>/', views.category, name='category'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('<int:post_pk>/scrapes/', views.scrapes, name='scrapes'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/create/<int:parent_pk>/', views.comment_create, name='comment_create'),
    path('<int:post_pk>/update/<int:comment_pk>/', views.comment_update, name='comment_update'),
    path('<int:post_pk>/delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
    path('<int:post_pk>/comment/<int:comment_pk>/likes/', views.comment_likes, name='comment_likes'),
    path('<int:post_pk>/comment/<int:comment_pk>/dislikes/', views.comment_dislikes, name='comment_dislikes'),
    # path('search/', views.search, name='search'),
    # path('tags/<int:tag_pk>/', views.tagged_posts, name='tagged_posts'),
    # path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    # path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
]
