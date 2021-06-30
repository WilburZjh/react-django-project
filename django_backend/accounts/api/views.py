from rest_framework import viewsets, status, permissions
from accounts.api.serializers import UserSerializer, LoginSerializer, SignupSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer

    @action(methods=['GET'], detail=False, url_path='login-status')
    def login_status(self, request):
        data = {
            "has_logged_in": request.user.is_authenticated,
            "ip": request.META['REMOTE_ADDR'],
        }

        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data

        return Response(data)

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({
            "success": True,
        }, status = status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Authentication is not recognized, please check your input",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "Username does not exist.",
            }, status = status.HTTP_400_BAD_REQUEST)

        user = django_authenticate(request, username=username, password=password)
        if not user:
            return Response({
                "success": False,
                "message": "Username and password do not match.",
            }, status = status.HTTP_400_BAD_REQUEST)

        django_login(request, user)
        return Response({
            "success": True,
            "message": "User has successfully logged in."
        }, status = status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please try again",
                "error": serializer.errors,
            }, status = status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        django_login(request, user)
        return Response({
            "success": True,
            "message": "Successfully signup and logged in."
        }, status = status.HTTP_200_OK)
