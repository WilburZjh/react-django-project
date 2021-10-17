from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
)

class CommentViewSet(viewsets.GenericViewSet):

    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(),]
        return [AllowAny(), ]

    # def list(self, request):
    #     data = {
    #
    #     }

    def create(self, request):
        print(request.data)
        data = {
            # 'user_id': request.user.id,
            # 'user_id': request.user,
            'tweet_id': request.data['tweet_id'],
            'content': request.data['content'],
        }
        serializer = CommentSerializerForCreate(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response({
                'Success': False,
                'Message': 'Can not create a comment.',
                'Error': serializer.errors,
            }, 400)

        comment = serializer.save()
        return Response({
            'Success': True,
            'Comment': CommentSerializer(comment).data
        })
