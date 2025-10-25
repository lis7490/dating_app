from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
#from .views import ProfileView


router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet, basename='profile')
router.register('photos', views.UserPhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/me/', views.CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('random-profile/', views.RandomProfileView.as_view(), name='random-profile'),
    path('preferences/', views.UserPreferencesView.as_view(), name='user-preferences'),
    #path('profile/', ProfileView.as_view(), name='profile'),
    path('verify-token/', views.verify_token, name='verify_token'),
]