from api.models import Invitation, User
from api.serializers.user_serializer import UserShortSerializer
from rest_framework import serializers


class InvitationSerializer(serializers.ModelSerializer):
    sender = UserShortSerializer(read_only=True)
    receiver = UserShortSerializer(read_only=True)
    class Meta:
        model = Invitation
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
        contact_request = Invitation.objects.create(
            name=name,
            sender=sender,
            receiver=receiver,
        )
        return contact_request
    
    
class InvitationCreateSerializer(serializers.ModelSerializer):
    sender = UserShortSerializer(read_only=True)
    receiver = UserShortSerializer(read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True, write_only=True)

    class Meta:
        model = Invitation
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

        contact_request = Invitation.objects.create(
            name=name,
            sender=sender,
            receiver=receiver,
        )
        
        return contact_request
