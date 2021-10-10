from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializer import UserSerializer, LoginSerializer, SignupSerializer
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny, )

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "Success": False,
                "Message": "Please check your input.",
                "Error": serializer.errors,
            }, status=400)

        username = serializer.validated_data['username']
        if not User.objects.filter(username = username).exists():
            return Response({
                "Success": False,
                "Message": "User does not exist."
            }, 400)

        password = serializer.validated_data['password']

        user = django_authenticate(request, username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                "Success": False,
                "Message": "Username and password do not match."
            }, status=400)

        django_login(request, user)
        return Response({
            "Has logged in": True,
            "User": UserSerializer(request.user).data,
        }, status=200)

    @action(methods=['GET'], detail=False)
    def check_status(self, request):
        data={'Has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "Success": False,
                "Message": "Username or email address has been occupied.",
                "Error": serializer.errors,
            }, 400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            "Success": True,
            "Message": "You have successfully signed up.",
            "User": UserSerializer(user).data,
        }, 200)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        if request.user.is_authenticated:
            django_logout(request)
            return Response({
                "Logged out": True,
                "Message": "You have successfully logged out."
            }, 200)
        return Response({
            "Logged out": False,
            "Message": "You need to log in before log out."
        }, 400)
