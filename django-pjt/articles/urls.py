from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:user_id>/articles/', views.user_articles, name='user_articles'),
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.article_comments),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.article_comment),
    path('<int:article_pk>/like/', views.article_likes),
]