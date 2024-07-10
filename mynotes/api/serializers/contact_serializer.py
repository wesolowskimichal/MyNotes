from rest_framework import serializers
from api.models import Contact
from api.serializers.user_serializer import UserShortSerializer

class ContactSerializer(serializers.ModelSerializer):
    user_from = UserShortSerializer(read_only=True)
    user_to = UserShortSerializer(read_only=True)
    
    class Meta:
        model = Contact
        fields = ['id', 'user_from', 'user_to', 'created']
        extra_kwargs = {
            'id': {'read_only': True},
            'user_from': {'read_only': True},
            'user_to': {'read_only': True},
            'created': {'read_only': True},
        }