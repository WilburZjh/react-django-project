from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from utils.mydecorator import verify_input

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    def create(self, validated_data):
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
        if User.objects.filter(username = attrs['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'Username is occupied.'
            })
        if User.objects.filter(email = attrs['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'Email is occupied.'
            })

        return attrs
