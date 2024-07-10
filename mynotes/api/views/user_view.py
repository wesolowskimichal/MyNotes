from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
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