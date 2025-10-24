from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('interactions', views.UserInteractionViewSet, basename='interaction')
router.register('matches', views.MatchViewSet, basename='match')
router.register('invitations', views.DateInvitationViewSet, basename='invitation')

urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:user_id>/', views.LikeUserView.as_view(), name='like-user'),
    path('dislike/<int:user_id>/', views.DislikeUserView.as_view(), name='dislike-user'),
    path('history/viewed/', views.ViewedProfilesView.as_view(), name='viewed-profiles'),
    path('history/liked/', views.LikedProfilesView.as_view(), name='liked-profiles'),
    path('history/disliked/', views.DislikedProfilesView.as_view(), name='disliked-profiles'),
    path('profile-likes/', views.ProfileLikesView.as_view(), name='profile-likes'),
]