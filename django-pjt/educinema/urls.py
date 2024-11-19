from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 관리자 페이지
    path('api/v1/admin/', admin.site.urls),

    # accounts 앱의 URL
    path('api/v1/accounts/', include('accounts.urls')),

    # 기타 앱의 URL
    path('api/v1/articles/', include('articles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)