from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    
    STATUS_CHOICES = [
        ('single', 'В активном поиске'),
        ('dating', 'Встречаюсь'),
        ('married', 'Женат/Замужем'),
        ('complicated', 'Все сложно'),
        ('not_looking', 'Не ищу отношения'),
    ]
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, default='')
    bio = models.TextField(max_length=500, blank=True)
    hobbies = models.TextField(max_length=1000, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='single')
    
    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    privacy_settings = models.CharField(max_length=10, default='public')
    show_online_status = models.BooleanField(default=True)
    allow_messages = models.BooleanField(default=True)
    
    is_verified = models.BooleanField(default=False)
    last_online = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = timezone.now().date()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

class UserPhoto(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='user_photos/')
    is_main = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'created_at']

    def save(self, *args, **kwargs):
        if self.is_main:
            UserPhoto.objects.filter(user_profile=self.user_profile, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo of {self.user_profile}"
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль при создании пользователя"""
    if created:
        try:
            # Используем get_or_create чтобы избежать ошибок при повторном создании
            UserProfile.objects.get_or_create(user=instance)
            print(f"✅ Автоматически создан профиль для {instance.username}")
        except Exception as e:
            print(f"❌ Ошибка создания профиля: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # Если профиль не существует, создаем его
        UserProfile.objects.create(user=instance)
        print(f"✅ Восстановлен профиль для {instance.username}")

# Добавьте в конец models.py
def check_all_profiles():
    """Проверка что у всех пользователей есть профили"""
    from django.contrib.auth.models import User
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            UserProfile.objects.create(user=user)
            print(f"✅ Создан отсутствующий профиль для {user.username}")

# Можно вызвать эту функцию при запуске
# check_all_profiles()

def get_user_profile(self):
    """Альтернативное property для доступа к профилю"""
    try:
        return self.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=self)
        print(f"🔄 Профиль принудительно создан для {self.username}")
        return profile

# Добавляем альтернативное property
User.add_to_class('get_profile', get_user_profile)