from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet


class TestCase(DjangoTestCase):

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
