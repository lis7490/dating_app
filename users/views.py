from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import UserProfile, UserPhoto
from .serializers import *
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes

from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
    # ГАРАНТИРУЕМ что профиль существует
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if created:
            print(f"🎯 Профиль создан через API для {self.request.user.username}")
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        # ГАРАНТИРУЕМ что профиль существует перед получением
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if created:
            print(f"🎯 Профиль создан через me() для {request.user.username}")
        
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
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if created:
            print(f"🎯 Профиль создан через CurrentUserProfileView для {self.request.user.username}")
        return profile

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
        # ГАРАНТИРУЕМ что профиль существует
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if created:
            print(f"🎯 Профиль создан через UserPhotoViewSet для {self.request.user.username}")
        return UserPhoto.objects.filter(user_profile=user_profile)

    def perform_create(self, serializer):
        # ГАРАНТИРУЕМ что профиль существует
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if created:
            print(f"🎯 Профиль создан при загрузке фото для {self.request.user.username}")
        serializer.save(user_profile=user_profile)
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ГАРАНТИРУЕМ что профиль существует
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if created:
            print(f"🎯 Профиль создан через ProfileView для {self.request.user.username}")
        context['user_profile'] = profile
        return context
    
def check_auth(request):
    """
    Проверка авторизации пользователя
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True, 
            'username': request.user.username,
            'user_id': request.user.id
        })
    else:
        return JsonResponse({
            'authenticated': False
        }, status=401)

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'profile.html'
    @api_view(['POST'])
    @permission_classes([])  # Разрешить доступ без аутентификации
    def verify_token(request):
        """Проверка валидности access token"""
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Проверяем токен
            access_token = AccessToken(token)
            # Если токен валиден, возвращаем успех
            return Response({
                'valid': True,
                'user_id': access_token['user_id']
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({
                'valid': False,
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET'])
def verify_token(request):
    """Простая проверка аутентификации"""
    if request.user.is_authenticated:
        return Response({'authenticated': True, 'user': request.user.username})
    else:
        return Response({'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED)