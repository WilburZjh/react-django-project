from rest_framework import serializers
from comments.models import Comment
from tweets.models import Tweet
from accounts.api.serializer import UserSerializerForComment
from rest_framework.exceptions import ValidationError
from likes.services import LikeService

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForComment()
    has_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model=Comment
        # 这里需要记住，tweet这个field返回的是ID，因为model中定义的是一个外键，而这个外键是一个ID
        # 这里如果继承的是Serializer，这些field都不会显示，需要自己手动显示。
        fields=(
            'id',
            'user',
            'tweet_id',
            'content',
            'created_at',
            'likes_count',
            'has_liked',
        )

    def get_has_liked(self, obj):
        return LikeService.has_liked(
            user=self.context['request'].user,
            target=obj,
        )

    def get_likes_count(self, obj):
        return obj.like_set.count()

class CommentSerializerForCreate(serializers.Serializer):
    tweet_id = serializers.IntegerField()
    # user_id = serializers.IntegerField()
    content = serializers.CharField(max_length=140)

    class Meta:
        model = Comment
        fields=('tweet_id', 'content')


    def validate(self, attrs):
        tweet_id = attrs['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise ValidationError({
                'Message': 'Tweet does not exist.',
            })
        return attrs


    def create(self, validated_data):
        return Comment.objects.create(
            # user = validated_data['user'],
            user = self.context['request'].user,
            tweet_id = validated_data['tweet_id'],
            content = validated_data['content'],
        )


class CommentSerializerForUpdate(serializers.Serializer):
    content=serializers.CharField(max_length=140)

    class Meta:
        model=Comment
        fields=('tweet_id', 'content', )

    def update(self, instance, validated_data):
        instance.content=validated_data['content']
        instance.save()
        return instance
