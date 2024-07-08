from rest_framework import serializers
from api.models import Group, User
from api.serializers.user_serializer import UserShortSerializer

class GroupDetailsSerializer(serializers.ModelSerializer):
    members = UserShortSerializer(many=True, read_only=True)
    owners = UserShortSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'image', 'members', 'owners']
        extra_kwargs = {
            'id': {'read_only': True}
        }

class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    owners = UserShortSerializer(many=True, read_only=True)
    members = UserShortSerializer(many=True, read_only=True)
    members_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False, write_only=True)
    owners_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False, write_only=True)
    member_groups_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False, write_only=True)
    owner_groups_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False, write_only=True)


    class Meta:
        model = Group
        fields = ['id', 'name', 'image', 'members', 'owners', 'members_ids', 'owners_ids', 'member_groups_ids', 'owner_groups_ids']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        members_ids = validated_data.pop('members_ids', [])
        owners_ids = validated_data.pop('owners_ids', [])
        member_groups_ids = validated_data.pop('member_groups_ids', [])
        owner_groups_ids = validated_data.pop('owner_groups_ids', [])
        group = Group.objects.create(
            name=validated_data.get('name'),
        )

        group.members.set(members_ids)
        group.owners.set(owners_ids)

        for group in member_groups_ids:
            group.members.add(*group.members.all())

        for group in owner_groups_ids:
            group.owners.add(*group.members.all())

        return group
    
    def update(self, instance, validated_data):
        members_ids = validated_data.pop('members_ids', [])
        owners_ids = validated_data.pop('owners_ids', [])
        member_groups_ids = validated_data.pop('member_groups_ids', [])
        owner_groups_ids = validated_data.pop('owner_groups_ids', [])

        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)

        if members_ids:
            instance.members.set(members_ids)
        if owners_ids:
            instance.owners.set(owners_ids)

        for group in member_groups_ids:
            group.members.add(*group.members.all())

        for group in owner_groups_ids:
            group.owners.add(*group.members.all())

        instance.save()
        return instance