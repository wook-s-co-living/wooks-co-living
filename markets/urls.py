from django.urls import path
from . import views

app_name="markets"
urlpatterns = [
    path('', views.market_index_view, name='market_index'),
    # path('<int:market_pk>/', views.market_detail_view, name='market_detail'),
    # path('create/', views.create_market_view, name='create_market'),
    # path('<int:market_pk>/delete/', views.delete_market_view, name='delete_market'),
    # path('<int:market_pk>/update/', views.update_market_view, name='update_market'),
    # path('<int:market_pk>/likes/', views.market_likes_view, name='market_likes'),
]
