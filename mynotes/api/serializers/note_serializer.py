from rest_framework import serializers
from api.models import Note, User, Group
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
    members = UserDetailsSerializer(many=True, read_only=True)
    owners = UserDetailsSerializer(many=True, read_only=True)
    members_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False, write_only=True)
    owners_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False, write_only=True)
    member_groups_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False, write_only=True)
    owner_groups_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False, write_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'htmlCode', 'nativeCode', 'members', 'owners', 'members_ids', 'owners_ids', 'member_groups_ids', 'owner_groups_ids']
        extra_kwargs = {
            'id': {'read_only': True},
            'htmlCode': {'read_only': True},
            'nativeCode': {'read_only': True},
        }


    def create(self, validated_data):
        members_ids = validated_data.pop('members_ids', [])
        owners_ids = validated_data.pop('owners_ids', [])
        member_groups_ids = validated_data.pop('member_groups_ids', [])
        owner_groups_ids = validated_data.pop('owner_groups_ids', [])
        note = Note.objects.create(
            title=validated_data.get('title'),
        )

        note.members.set(members_ids)
        note.owners.set(owners_ids)

        for group in member_groups_ids:
            note.members.add(*group.members.all())

        for group in owner_groups_ids:
            note.owners.add(*group.members.all())

        return note