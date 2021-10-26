from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.api.permissions import IsObjectOwner
from rest_framework.response import Response
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from utils.mydecorator import required_params

class CommentViewSet(viewsets.GenericViewSet):

    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()
    filterset_fields = ('tweet_id', )

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(),]
        if self.action in ['update', 'destroy']:
            return [IsAuthenticated(), IsObjectOwner(),]
        return [AllowAny(), ]


    @required_params(params=['tweet_id'])
    def list(self, request, *args, **kwargs):
        # if 'tweet_id' not in request.query_params:
        #     return Response({
        #         'Success': False,
        #         'Message': 'Missing tweet id information.'
        #     }, 400)

        queryset=self.get_queryset()
        comments=self.filter_queryset(queryset).prefetch_related('user').order_by('created_at')
        return Response({
            'Comment': CommentSerializer(
                comments,
                context={'request':request},
                many=True,
            ).data,
        })

    def create(self, request):
        """
        print(request.data) =>
        <QueryDict: {
            'csrfmiddlewaretoken': ['kqJP4BuCHqYF9c8Y6Jqq9rmgPAeLoqpFUV0UOlDbSbIYfC1RGRqeKfuHGT5Iptgi'], 
            'tweet_id': ['4'], 
            'content': ['admin-second-comment-on-zjh-second-tweet']
            }
        >
        """
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
        # print(CommentSerializer(comment))
        # print(CommentSerializer(comment).data)
        """
        print(CommentSerializer(comment)) => 
        CommentSerializer(<Comment: 2021-10-18 00:14:48.650528+00:00 - admin says admin-second-comment-on-zjh-second-tweet at tweet 2021-10-15 23:24:28.973521+00:00 zjh: zjh-second-tweet>):
    id = IntegerField(label='ID', read_only=True)
    user = UserSerializerForComment():
        id = IntegerField(label='ID', read_only=True)
        username = CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[<django.contrib.auth.validators.UnicodeUsernameValidator object>, <UniqueValidator(queryset=User.objects.all())>])
    tweet_id = ReadOnlyField()
    content = CharField(max_length=140)
    created_at = DateTimeField(read_only=True)
        ----------------------------------------------------------------------------------------------------------------
        print(CommentSerializer(comment).data) =>
        {
            'id': 7, 
            'user': OrderedDict([
                        ('id', 1), 
                        ('username', 'admin')
                    ]), 
            'tweet_id': 4, 
            'content': 'admin-second-comment-on-zjh-second-tweet', 
            'created_at': '2021-10-18T00:14:48.650528Z'
        }
        """
        return Response({
            'Success': True,
            'Comment': CommentSerializer(
                comment,
                context={'request': request},
            ).data
        })


    def update(self, request, *args, **kargs):
        pk = self.get_object()
        serializer=CommentSerializerForUpdate(
            instance=pk,
            data=request.data
        )

        if not serializer.is_valid():
            return Response({
                'Success': False,
                'Message': 'Update fail',
                'Error': serializer.errors,
            }, 400)

        comment = serializer.save()
        return Response({
            'Success': True,
            'Updated comment': CommentSerializer(
                comment,
                context={'request': request},
            ).data
        }, 200)


    def destroy(self, request, *args, **kwargs):
        pk = self.get_object()
        pk.delete()
        return Response({
            'Success': True
        }, 200)
