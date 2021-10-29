from rest_framework import serializers
from rest_framework.serializers import ValidationError
from likes.models import Like
from accounts.api.serializer import UserSerializerForLike
from django.contrib.contenttypes.models import ContentType
from tweets.models import Tweet
from comments.models import Comment

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializerForLike()

    class Meta:
        model=Like
        fields=('user', 'created_at')

class BaseLikeSerializerForCreateAndCancel(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(choices=['comment', 'tweet'])
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('content_type', 'object_id')

    def _get_model_class(self, data):
        if data['content_type'] is 'tweet':
            return Tweet
        if data['content_type'] is 'comment':
            return Comment
        return None

    def validate(self, attrs):
        model_class = self._get_model_class(attrs)
        if model_class is None:
            raise ValidationError({
                'content_type': '{} is not a valid model name.'.format(attrs['content_type']),
            })

        instance = model_class.objects.filter(id=attrs['object_id']).first()
        if instance is None:
            raise ValidationError({
                'object_id': '{} does not contain {}.'.format(model_class.__class__, attrs['object_id'])
            })
        return attrs

class LikeSerializerForCreate(BaseLikeSerializerForCreateAndCancel):

    def get_or_create(self):
        model_class=self._get_model_class(self.validated_data)
        return Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(model_class),
            object_id=self.validated_data['object_id'],
            user=self.context['request'].user,
        )

class LikeSerializerForCancel(BaseLikeSerializerForCreateAndCancel):

    def cancel(self):
        model_class=self._get_model_class(self.validated_data)
        deleted, _ = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(model_class),
            object_id=self.validated_data['object_id'],
            user=self.context['request'].user,
        ).delete()

        return deleted
