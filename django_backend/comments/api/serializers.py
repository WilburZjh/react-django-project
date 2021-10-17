from rest_framework import serializers
from comments.models import Comment
from tweets.models import Tweet
from tweets.api.serializer import TweetSerializer
from accounts.api.serializer import UserSerializerForComment
from rest_framework.exceptions import ValidationError


class CommentSerializer(serializers.Serializer):
    user = UserSerializerForComment()
    tweet = TweetSerializer()
    class Meta:
        model=Comment
        fields=('id', 'user', 'tweet', 'content', 'created_at')


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
