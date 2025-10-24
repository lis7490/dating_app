from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/interactions/', include('interactions.urls')),
    
    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Главная и веб-страницы
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('discover/', TemplateView.as_view(template_name='discover.html'), name='discover'),
    path('matches/', TemplateView.as_view(template_name='matches.html'), name='matches'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('history/', TemplateView.as_view(template_name='history.html'), name='history'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='settings'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('check-auth/', views.check_auth, name='check_auth'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)