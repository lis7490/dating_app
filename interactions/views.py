from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import UserInteraction, Match, DateInvitation
from users.models import UserProfile
from .serializers import *

class UserInteractionViewSet(viewsets.ModelViewSet):
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInteraction.objects.filter(from_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class LikeUserView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInteractionSerializer

    def create(self, request, user_id=None):
        try:
            to_user_profile = UserProfile.objects.get(user_id=user_id)
            to_user = to_user_profile.user
            
            # Проверяем, не существует ли уже взаимодействие
            interaction, created = UserInteraction.objects.get_or_create(
                from_user=request.user,
                to_user=to_user,
                defaults={'interaction_type': 'like'}
            )
            
            if not created:
                return Response(
                    {'error': 'Interaction already exists'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Увеличиваем счетчик лайков
            to_user_profile.likes_count += 1
            to_user_profile.save()
            
            # Проверяем взаимный лайк
            mutual_like = UserInteraction.objects.filter(
                from_user=to_user,
                to_user=request.user,
                interaction_type='like'
            ).exists()
            
            response_data = {
                'status': 'liked',
                'mutual_match': mutual_like
            }
            
            if mutual_like:
                # Создаем мэтч
                match = Match.objects.create()
                match.users.add(request.user, to_user)
                response_data['match_id'] = match.id
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class DislikeUserView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, user_id=None):
        try:
            to_user = UserProfile.objects.get(user_id=user_id).user
            
            interaction, created = UserInteraction.objects.get_or_create(
                from_user=request.user,
                to_user=to_user,
                defaults={'interaction_type': 'dislike'}
            )
            
            if not created:
                interaction.interaction_type = 'dislike'
                interaction.save()
            
            return Response({'status': 'disliked'}, status=status.HTTP_201_CREATED)
            
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ViewedProfilesView(generics.ListAPIView):
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInteraction.objects.filter(from_user=self.request.user)

class LikedProfilesView(generics.ListAPIView):
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInteraction.objects.filter(
            from_user=self.request.user,
            interaction_type='like'
        )

class DislikedProfilesView(generics.ListAPIView):
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInteraction.objects.filter(
            from_user=self.request.user,
            interaction_type='dislike'
        )

class ProfileLikesView(generics.ListAPIView):
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInteraction.objects.filter(
            to_user=self.request.user,
            interaction_type='like'
        )

class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Match.objects.filter(users=self.request.user)

class DateInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = DateInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DateInvitation.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if invitation.to_user != request.user:
            return Response(
                {'error': 'Not allowed'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        invitation.status = 'accepted'
        invitation.save()
        return Response({'status': 'invitation accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        invitation = self.get_object()
        if invitation.to_user != request.user:
            return Response(
                {'error': 'Not allowed'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        invitation.status = 'rejected'
        invitation.save()
        return Response({'status': 'invitation rejected'})