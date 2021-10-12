from rest_framework import viewsets
from tweets.api.serializer import TweetSerializer, TweetSerializerForCreate
from rest_framework.response import Response
from tweets.models import Tweet
from rest_framework.permissions import IsAuthenticated, AllowAny


class TweetViewSet(viewsets.GenericViewSet):

    serializer_class = TweetSerializerForCreate

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request):
        if not request.user.is_authenticated:
            return Response({'Please login first'}, 400)

        if 'user_id' not in request.query_params:
            return Response({'Missing user id.'}, 400)

        user_id = request.query_params['user_id']
        queries = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        return Response({'Tweets:': TweetSerializer(queries, many=True).data}, 200)

    def create(self, request):
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                "Success": False,
                "Message": "Please check the content.",
                "Errors": serializer.errors,
            })
        tweet = serializer.save()
        return Response({
            "Success": True,
            "Content": TweetSerializer(tweet).data,
        }, 201)
