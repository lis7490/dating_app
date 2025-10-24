from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    
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
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
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