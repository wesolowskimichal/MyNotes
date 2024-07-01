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
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    owners = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Group
        fields = ['name', 'image', 'members', 'owners']