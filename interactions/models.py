from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class UserView(models.Model):
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='viewed_profiles')
    viewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='viewers')
    viewed_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)

    class Meta:
        unique_together = ['viewer', 'viewed_user']
        ordering = ['-viewed_at']

class Like(models.Model):
    LIKED = 'like'
    DISLIKED = 'dislike'
    SUPERLIKE = 'superlike'
    
    LIKE_TYPES = [
        (LIKED, 'Лайк'),
        (DISLIKED, 'Дизлайк'),
        (SUPERLIKE, 'Суперлайк'),
    ]
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_likes')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_likes')
    like_type = models.CharField(max_length=10, choices=LIKE_TYPES, default=LIKED)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']

class Match(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='matches')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

class UserInteraction(models.Model):
    INTERACTION_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_interactions')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.interaction_type})"
    
class DateInvitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invitation from {self.from_user} to {self.to_user}"