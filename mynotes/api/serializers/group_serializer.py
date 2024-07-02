from rest_framework import serializers
from api.models import Group, User
from api.serializers.user_serializer import UserDetailsSerializer

class GroupDetailsSerializer(serializers.ModelSerializer):
    members = UserDetailsSerializer(many=True, read_only=True)
    owners = UserDetailsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'image', 'members', 'owners']
        extra_kwargs = {
            'id': {'read_only': True}
        }

class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    members_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    owners_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    members = UserDetailsSerializer(many=True, read_only=True)
    owners = UserDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'image', 'members', 'owners', 'members_ids', 'owners_ids']
        extra_kwargs = {
            'id': {'read_only': True}
        }