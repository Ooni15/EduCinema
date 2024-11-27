from django.urls import path
from . import views


urlpatterns = [
    path('user/<int:user_id>/articles/', views.user_articles, name='user_articles'),
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.article_comments),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.article_comment),
    path('<int:article_pk>/like/', views.article_likes),
    path('recommendations/', views.get_article_recommendations, name='article-recommendations'),
    path('<int:article_pk>/gpt-query/', views.article_gpt_query, name='article_gpt_query'),
]