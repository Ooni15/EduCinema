from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user-list'),  # 사용자 리스트 조회
    path('signup/', views.signup, name='signup'),  # 회원가입
    path('login/', views.login, name='login'),  # 로그인
    path('logout/', views.logout, name='logout'),
    path('users/<int:user_pk>/', views.user_detail, name='user-detail'),  # 사용자 상세 조회, 수정, 삭제
    path('users/<int:user_id>/comments/', views.profile_comments, name='profile-comments'),
    path('comments/<int:comment_id>/', views.profile_comment_detail, name='profile-comment-detail'),
    path('users/<int:user_id>/toggle-like/', views.toggle_like, name='toggle-like'),
    path('me/', views.get_current_user, name='current_user'),
]
