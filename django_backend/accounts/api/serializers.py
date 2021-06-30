from rest_framework import serializers, exceptions, status
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=20)
    password = serializers.CharField(min_length=3, max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, data):
        username=data['username']
        email=data['email']

        if User.objects.filter(username=username).exists():
            raise exceptions.ValidationError({
                "message": "This username is occupied",
            })

        if User.objects.filter(email=email).exists():
            raise exceptions.ValidationError({
                "message": "This email address is occupied",
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        password = validated_data['password']
        email = validated_data['email']

        user = User.objects.create_user(username=username, email=email, password=password)
        return user
