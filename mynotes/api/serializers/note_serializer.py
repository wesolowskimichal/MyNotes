from rest_framework import serializers
from api.models import Note, User
from api.serializers.user_serializer import UserDetailsSerializer


class NoteDetailsSerializer(serializers.ModelSerializer):
    members = UserDetailsSerializer(many=True, read_only=True)
    owners = UserDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'htmlCode', 'nativeCode', 'members', 'owners']
        extra_kwargs = {
            'id': {'read_only': True},
            'htmlCode': {'read_only': True},
            'nativeCode': {'read_only': True}
        }

class NoteCreateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    owners = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Note
        fields = ['id', 'title', 'htmlCode', 'nativeCode', 'members', 'owners']
        extra_kwargs = {
            'id': {'read_only': True},
            'htmlCode': {'read_only': True},
            'nativeCode': {'read_only': True}
        }