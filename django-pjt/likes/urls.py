from django.urls import path
from . import views

urlpatterns = [
    # # 전체 영화 목록 조회         # 임시
    # path('', views.movie_list, name='movie-list'),
    # # 특정 영화 상세 정보 조회 (연관 기술 포함)
    # path('<int:movie_pk>/', views.movie_detail, name='movie-detail'),
]