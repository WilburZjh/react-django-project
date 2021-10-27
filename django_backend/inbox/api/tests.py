from testing.testcases import TestCase
from notifications.models import Notification


COMMENT_URL = '/api/comments/'
LIKE_URL = '/api/likes/'

class NotificationAPITest(TestCase):

    def setUp(self):
        self.user1, self.user1_client = self.create_user_and_client('user1')
        self.user2, self.user2_client = self.create_user_and_client('user2')
        self.user1_tweet = self.create_tweet(user=self.user1)

    def test_comment_create_api_trigger_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.user1_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'a ha',
        })
        self.assertEqual(Notification.objects.count(), 0)

        self.user2_client.post(COMMENT_URL, {
            'tweet_id': self.user1_tweet.id,
            'content': 'a ha',
        })
        self.assertEqual(Notification.objects.count(), 1)

    def test_like_create_api_trigger_notification(self):
        self.assertEqual(Notification.objects.count(), 0)
        self.user1_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        self.assertEqual(Notification.objects.count(), 0)

        self.user2_client.post(LIKE_URL, {
            'content_type': 'tweet',
            'object_id': self.user1_tweet.id,
        })
        self.assertEqual(Notification.objects.count(), 1)

        user1_comment = self.create_comment(self.user1, self.user1_tweet)
        self.user1_client.post(LIKE_URL, {
            'content_type': 'comment',
            'object_id': user1_comment.id,
        })
        self.assertEqual(Notification.objects.count(), 1)

        user2_comment = self.create_comment(self.user2, self.user1_tweet)
        self.user1_client.post(LIKE_URL, {
            'content_type': 'comment',
            'object_id': user2_comment.id,
        })
        self.assertEqual(Notification.objects.count(), 2)
