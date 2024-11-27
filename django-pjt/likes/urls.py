from django.urls import path
from . import views

urlpatterns = [
    path('', views.likes_list),  # 전체 좋아요 목록
    path('<int:like_pk>/', views.likes_detail),  # 특정 좋아요 상세
    path('<int:article_pk>/likes/', views.article_likes),  # 특정 게시글의 좋아요 상태
]