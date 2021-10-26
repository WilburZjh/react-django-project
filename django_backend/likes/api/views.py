from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from likes.models import Like
from likes.api.serializers import (
    LikeSerializer,
    LikeSerializerForCreate,
    LikeSerializerForCancel,
)
from rest_framework.response import Response
from utils.mydecorator import required_params

class LikeViewSet(viewsets.GenericViewSet):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializerForCreate

    @required_params(request_attrs='data', params=['content_type', 'object_id'])
    def create(self, request):
        serializer = LikeSerializerForCreate(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response({
                'Success': False,
                'Message': 'You can not create.',
                'Error': serializer.errors,
            }, 400)

        instance = serializer.save()
        return Response({
            'Success': True,
            'Like': LikeSerializer(instance).data,
        }, 201)


    @action(methods=['POST'], detail=False)
    @required_params(request_attrs='data', params=['content_type', 'object_id'])
    def cancel(self, request):
        serializer = LikeSerializerForCancel(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'Success': False,
                'Message': 'You can not cancel.',
                'Error': serializer.errors,
            }, 400)

        deleted = serializer.cancel()
        return Response({
            'Success': True,
            'Delete': deleted,
        })
