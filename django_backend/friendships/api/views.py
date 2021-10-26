from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from friendships.api.serializers import (
    FollowerSerializer,
    FollowingSerializer,
    FriendshipSerializerForCreate,
)
from rest_framework.response import Response
from friendships.models import Friendship

class FriendshipViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = FriendshipSerializerForCreate

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny,])
    def followings(self, request, pk):
        queries = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')
        serializer = FollowingSerializer(queries, many=True)
        return Response({
            'Success': True,
            'Followings': serializer.data,
        }, status=200)


    @action(methods=['GET'], detail=True, permission_classes=[AllowAny,])
    def followers(self, request, pk):
        queries = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowerSerializer(queries, many=True)
        return Response({
            'Success': True,
            'Followers': serializer.data,
        }, status=200)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated,])
    def follow(self, request, pk):
        follow_user = self.get_object()
        if Friendship.objects.filter(from_user=request.user, to_user=follow_user).exists():
            return Response({
                'Success': True,
                'Duplicate': True,
            }, status=201)

        serializer = FriendshipSerializerForCreate(data={
            'from_user_id': request.user.id,
            'to_user_id': follow_user.id,
        })

        if not serializer.is_valid():
            return Response({
                'Success': False,
                'Message': '{} can not follow {}'.format(request.user.id, follow_user.id),
                'Error': serializer.errors,
            }, 400)

        friendship = serializer.save()
        return Response({
            'Success': True,
            'Message': '{} is following {} now'.format(request.user, follow_user),
        }, status=200)


    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated,])
    def unfollow(self, request, pk):
        unfollow_user = self.get_object() # pk
        # print(type(unfollow_user))
        if request.user.id == unfollow_user.id:
            return Response({
                'success': False,
                'message': 'You cannot unfollow yourself',
            }, status=400)

        deleted, _ = Friendship.objects.filter(
            from_user_id = request.user.id,
            to_user_id = pk,
        ).delete()
        return Response({
            'Success': True,
            'Message': '{} unfollows {}'.format(request.user.id, pk)
        })
