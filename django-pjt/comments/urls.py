from django.urls import path
from . import views

urlpatterns = [
    path('', views.comment_list),
    path('<int:comment_pk>/', views.comment_detail),
    path('articles/<int:article_pk>/comments/', views.article_comments),  # 특정 게시글의 댓글 목록
]