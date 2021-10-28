from rest_framework import serializers
from accounts.api.serializer import UserSerializerForTweet
from tweets.models import Tweet
from comments.api.serializers import CommentSerializer
from likes.services import LikeService
from likes.api.serializers import LikeSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet() # used to deep check the user from tweet model. call serializer inside another serializer.
    has_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()


    class Meta:
        model = Tweet
        fields = (
            'id',
            'user',
            'created_at',
            'content',
            'comments_count',
            'likes_count',
            'has_liked',
        )

    # 自定义的like_set。
    def get_likes_count(self, obj):
        return obj.like_set.count()

    # Django提供的comment_set。
    def get_comments_count(self, obj):
        return obj.comment_set.count();

    def get_has_liked(self, obj):
        return LikeService.has_liked(
            user=self.context['request'].user,
            target=obj,
        )

class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)
    class Meta:
        model = Tweet
        fields = ('content', )

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet


class TweetSerializerForDetail(TweetSerializer):
    comments = CommentSerializer(source='comment_set', many=True)
    likes = LikeSerializer(source='like_set', many=True)

    class Meta:
        model = Tweet
        fields = (
            'id',
            'user',
            'comments',
            'created_at',
            'content',
            'likes',
            'likes_count',
            'comments_count',
            'has_liked',
        )
