from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import UserProfile, UserPhoto

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ['id', 'image', 'is_main', 'caption', 'created_at']
        read_only_fields = ['created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    age = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'first_name', 'last_name', 'email', 'gender', 'age', 'city',
            'bio', 'hobbies', 'status', 'likes_count', 'views_count'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Поля профиля
    gender = serializers.CharField(write_only=True, required=True)
    birth_date = serializers.DateField(write_only=True, required=True)
    city = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 
                 'gender', 'birth_date', 'city']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        # Извлекаем данные профиля
        gender = validated_data.pop('gender')
        birth_date = validated_data.pop('birth_date')
        city = validated_data.pop('city')
        validated_data.pop('password2')
        
        # Создаем пользователя
        user = User.objects.create_user(
            username=validated_data['email'],  # Используем email как username
            **validated_data
        )
        
        # Создаем профиль
        UserProfile.objects.create(
            user=user,
            gender=gender,
            birth_date=birth_date,
            city=city
        )
        
        return user
class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'preferred_gender', 'preferred_min_age', 'preferred_max_age',
            'preferred_city', 'search_radius_km'
        ]