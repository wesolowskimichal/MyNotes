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

class ContactListSerializer(serializers.ModelSerializer):
    user_from = UserShortSerializer(read_only=True)
    user_to = UserShortSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'user_from', 'user_to']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        user = request.user

        if str(representation['user_from']['id']) == str(user.id):
            user_data = representation.pop('user_to', None)
            representation.pop('user_from')
        else:
            user_data = representation.pop('user_from', None)
            representation.pop('user_to')
        
        if user_data:
            representation['user'] = user_data
        else:
            representation['user'] = None 

        return representation