from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from utils.mydecorator import verify_input
from accounts.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserSerializerWithProfile(serializers.ModelSerializer):
    nickname = serializers.CharField(source='profile.nickname')
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        if obj.profile.avatar:
            return obj.profile.avatar.url
        return None

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'avatar_url')


class UserSerializerForTweet(UserSerializerWithProfile):
    pass


class UserSerializerForFriendship(UserSerializerWithProfile):
    pass


class UserSerializerForComment(UserSerializerWithProfile):
    pass


class UserSerializerForLike(UserSerializerWithProfile):
    pass


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        # print(validated_data)
        username = validated_data['username'].lower()
        password = validated_data['password']
        email = validated_data['email'].lower()

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        return user

    @verify_input
    def validate(self, attrs):
        # print(attrs, type(attrs))
        if User.objects.filter(username = attrs['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'Username is occupied.'
            })
        if User.objects.filter(email = attrs['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'Email is occupied.'
            })

        return attrs


class UserProfileSerializerForUpdate(serializers.ModelSerializer):

    class Meta:
        model=UserProfile
        fields=('nickname', 'avatar')
