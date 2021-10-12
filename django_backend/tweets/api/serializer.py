from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action
from accounts.api.serializer import UserSerializerForTweet
from tweets.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet() # used to deep check the user from tweet model. call serializer inside another serializer.

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')

class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(max_length=140)
    class Meta:
        model = Tweet
        fields = ('content', )

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet
