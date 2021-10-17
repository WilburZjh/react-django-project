from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from comments.models import Comment
from rest_framework.test import APIClient


class TestCase(DjangoTestCase):

    @property
    def anonymous_client(self):
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_user(self, username, email = None, password = None):
        if email is None:
            email = 'testtweet@reactdjango.com'

        if password is None:
            password = 'generic password'

        return User.objects.create_user(
            username = username,
            password = password,
            email = email,
        )

    def create_tweet(self, user, content=None):
        if content is None:
            content = 'test content'

        return Tweet.objects.create(
            user = user,
            content = content,
        )

    def create_comment(self, user, tweet, content=None):
        if content is None:
            content='default comments'
        return Comment.objects.create(user=user, tweet=tweet, content=content)
