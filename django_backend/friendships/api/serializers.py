from rest_framework import serializers
from accounts.api.serializer import UserSerializerForFriendship
from friendships.models import Friendship
from rest_framework.exceptions import ValidationError


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializerForFriendship(source='from_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model=Friendship
        fields=('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializerForFriendship(source='to_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model=Friendship
        fields=('user', 'created_at')

class FriendshipSerializerForCreate(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ('from_user_id', 'to_user_id')

    def create(self, validated_data):
        from_user_id = validated_data['from_user_id']
        to_user_id = validated_data['to_user_id']

        friendship = Friendship.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
        )
        return friendship

    def validate(self, attrs):
        if attrs['from_user_id'] == attrs['to_user_id']:
            raise ValidationError({
                'Message': 'From_user_id and to_user_id should be different.',
            })
        return attrs
