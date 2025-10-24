from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import UserProfile, UserPhoto
from .serializers import *
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        profile = UserProfile.objects.get(user=request.user)
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

class RandomProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем фильтры из query parameters
        gender = self.request.query_params.get('gender')
        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')
        city = self.request.query_params.get('city')
        
        # Базовый запрос - исключаем текущего пользователя и уже просмотренных
        from interactions.models import UserInteraction
        viewed_users = UserInteraction.objects.filter(
            from_user=self.request.user
        ).values_list('to_user', flat=True)
        
        queryset = UserProfile.objects.exclude(
            Q(user=self.request.user) | Q(user__in=viewed_users)
        )
        
        # Применяем фильтры
        if gender:
            queryset = queryset.filter(gender=gender)
        if min_age:
            queryset = queryset.filter(age__gte=int(min_age))
        if max_age:
            queryset = queryset.filter(age__lte=int(max_age))
        if city:
            queryset = queryset.filter(city__iexact=city)
        
        # Возвращаем случайный профиль
        return queryset.order_by('?').first()

class UserPreferencesView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class UserPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UserPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем UserProfile текущего пользователя и фильтруем по нему
        user_profile = UserProfile.objects.get(user=self.request.user)
        return UserPhoto.objects.filter(user_profile=user_profile)

    def perform_create(self, serializer):
        # Сохраняем с правильным user_profile
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user_profile=user_profile)

    @action(detail=True, methods=['post'])
    def set_main(self, request, pk=None):
        photo = self.get_object()
        # Сбрасываем все фото как не основные для этого пользователя
        user_profile = UserProfile.objects.get(user=request.user)
        UserPhoto.objects.filter(user_profile=user_profile).update(is_main=False)
        # Устанавливаем текущее как основное
        photo.is_main = True
        photo.save()
        return Response({'status': 'main photo set'})
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        return context