from django.utils import timezone
from rest_framework import serializers
from api.models import User, ContactRequest

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'image']

class ContactRequestSerializer(serializers.ModelSerializer):
    sender = UserShortSerializer(many=True, read_only=True)
    receiver = UserShortSerializer(many=True, read_only=True)
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'sender', 'receiver', 'sent_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'sent_at': {'read_only': True}
        }
    
    def create(self, validated_data):
        sender = validated_data['sender']
        receiver = validated_data['receiver']
        name = f'{sender.first_name} {sender.last_name} has invited {receiver.first_name} {receiver.last_name} to contacts'
        contact_request = ContactRequest.objects.create(
            name=name,
            sender=sender,
            receiver=receiver,
            sent_at=validated_data.get('sent_at', timezone.now())
        )
        return contact_request
    
class ContactRequestCreateSerializer(serializers.ModelSerializer):
    sender = UserShortSerializer(read_only=True)
    receiver = UserShortSerializer(read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True, write_only=True)

    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'sender', 'receiver', 'receiver_id', 'sent_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'sent_at': {'read_only': True}
        }

    def create(self, validated_data):
        receiver = validated_data.get('receiver_id')
        sender = self.context['request'].user
        name = f'{sender.first_name} {sender.last_name} has invited {receiver.first_name} {receiver.last_name} to contacts'

        contact_request = ContactRequest.objects.create(
            name=name,
            sender=sender,
            receiver=receiver,
            sent_at=timezone.now()
        )
        
        return contact_request



class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image']
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
        }

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'image']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        
        return user