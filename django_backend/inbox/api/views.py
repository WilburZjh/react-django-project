from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from inbox.api.serializers import (
    NotificationSerializer,
    NotificationSerializerForUpdate,
)
from notifications.models import Notification
from utils.mydecorator import required_params


class NotificationViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,]
    filterset_fields=('unread', )

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(methods=['GET'], detail=False, url_path='unread-count')
    def unread_count(self, request, *args, **kwargs):
        return Response({
            'unread_count': self.get_queryset().filter(unread=True).count(),
        }, 200)

    @action(methods=['POST'], detail=False, url_path='mark-all-as-read')
    def mark_all_as_read(self, request, *args, **kwargs):
        return Response({
            'marked_count': self.get_queryset().filter(unread=True).update(unread=False),
        }, 200)

    @required_params(method='PUT', params=['unread'])
    def update(self, request, *args, **kwargs):
        pk = self.get_object()

        serializer = NotificationSerializerForUpdate(
            instance=pk,
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'Success': False,
                'Message': 'Can not update',
                'Error': serializer.errors,
            }, 400)

        instance=serializer.save()
        return Response(NotificationSerializer(instance).data, 200)
