from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name="accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('check/', views.check, name='check'),
    path('id_overlap_check/', views.id_overlap_check, name='id_overlap_check'),
    path('email_overlap_check/', views.email_overlap_check, name='email_overlap_check'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('delete/', views.delete, name='delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/followers-list/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/likes/', views.user_likes, name='user_likes'),
    path('profile/<str:username>/dislikes/', views.user_dislikes, name='user_dislikes'),
    path('activate/<str:token>/', views.activate, name='activate'),

    # 비밀번호 재설정
    path('password_reset/', views.password_reset_request, name="password_reset"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
]
