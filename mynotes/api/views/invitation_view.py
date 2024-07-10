from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers.user_serializer import *
from api.models import Contact, Invitation
from api.serializers.invitation_serializer import InvitationCreateSerializer, InvitationSerializer

class InviteView(generics.CreateAPIView):
    serializer_class = InvitationCreateSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        user = self.request.user
        receiver = serializer.validated_data['receiver_id']

        if user == receiver:
            raise serializers.ValidationError({"detail": "You cannot send a contact invitation to yourself."})
        
        if Contact.objects.filter(user_from=user, user_to=receiver).exists() or Contact.objects.filter(user_from=receiver, user_to=user).exists():
            raise serializers.ValidationError({"detail": "You cannot send a contact invitation to someone that you already have in contacts."}) 

        if Invitation.objects.filter(sender=user, receiver=receiver).exists():
            raise serializers.ValidationError({"detail": "You have already sent a contact invitation to this user."})
        
        serializer.save(sender=user, receiver=receiver)


class InvitationsReceivedView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(receiver=user)
    
class InvitationsSentView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(sender=user)


class InvitationAcceptView(generics.DestroyAPIView):
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(receiver=user)
    
    def destroy(self, request, *args, **kwargs):
        contact_request = self.get_object()
        contact_request.accept()
        return Response({'status': 'Invitation accepted'}, status=status.HTTP_200_OK)
    

class InvitationDenyView(generics.DestroyAPIView):
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(receiver=user)
    
    def destroy(self, request, *args, **kwargs):
        contact_request = self.get_object()
        contact_request.deny()
        return Response({'status': 'Invitation denied'}, status=status.HTTP_200_OK)