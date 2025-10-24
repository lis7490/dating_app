from rest_framework import serializers
from .models import UserInteraction, Match, DateInvitation
from users.serializers import UserProfileSerializer

class UserInteractionSerializer(serializers.ModelSerializer):
    to_user_profile = UserProfileSerializer(source='to_user.userprofile', read_only=True)
    
    class Meta:
        model = UserInteraction
        fields = ['id', 'to_user', 'to_user_profile', 'interaction_type', 'created_at']
        read_only_fields = ['created_at']

class MatchSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'users', 'other_user', 'created_at']
        read_only_fields = ['created_at']

    def get_other_user(self, obj):
        request = self.context.get('request')
        if request and request.user:
            other_user = obj.users.exclude(id=request.user.id).first()
            if other_user:
                return UserProfileSerializer(other_user.userprofile).data
        return None

class DateInvitationSerializer(serializers.ModelSerializer):
    from_user_profile = UserProfileSerializer(source='from_user.userprofile', read_only=True)
    to_user_profile = UserProfileSerializer(source='to_user.userprofile', read_only=True)

    class Meta:
        model = DateInvitation
        fields = [
            'id', 'from_user', 'from_user_profile', 'to_user', 'to_user_profile',
            'message', 'status', 'created_at'
        ]
        read_only_fields = ['created_at']