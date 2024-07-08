from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from api.serializers.user_serializer import *

class UserContactListView(generics.ListAPIView):
    """
    Receiving contacts list of currently logged User
    """
    serializer_class = UserShortSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.contacts.all()
    
class UserContactsInvite(generics.ListCreateAPIView):
    serializer_class = ContactRequestCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ContactRequest.objects.filter(sender=user)

    def perform_create(self, serializer):
        user = self.request.user
        receiver = serializer.validated_data['receiver_id']

        if user == receiver:
            raise serializers.ValidationError({"detail": "You cannot send a contact request to yourself."})

        
        # Check if a contact request already exists
        if ContactRequest.objects.filter(sender=user, receiver=receiver).exists():
            raise serializers.ValidationError({"detail": "You have already sent a contact request to this user."})
        
        
        serializer.save(sender=user, receiver=receiver)

class UserRegisterView(generics.CreateAPIView):
    """
    Creating new User
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Managing currently logged User
    """
    
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        return user