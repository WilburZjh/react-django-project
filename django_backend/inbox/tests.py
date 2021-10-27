from testing.testcases import TestCase
from inbox.services import NotificationService
from notifications.models import Notification

# Create your tests here.
class NotificationServiceTest(TestCase):

    def setUp(self):
        self.user1 = self.create_user('user1')
        self.user2 = self.create_user('user2')
        self.user1_tweet = self.create_tweet(
            user=self.user1,
        )

    def test_send_like_notification(self):
        user1_liked_tweet = self.create_like(
            user=self.user1,
            target=self.user1_tweet,
        )
        NotificationService.send_like_notification(user1_liked_tweet)
        self.assertEqual(Notification.objects.count(), 0)

        user2_liked_tweet = self.create_like(
            user=self.user2,
            target=self.user1_tweet,
        )
        NotificationService.send_like_notification(user2_liked_tweet)
        self.assertEqual(Notification.objects.count(), 1)

    def test_send_comment_notification(self):
        user1_comment_tweet = self.create_comment(
            user=self.user1,
            tweet=self.user1_tweet,
        )
        NotificationService.send_comment_notification(user1_comment_tweet)
        self.assertEqual(Notification.objects.count(), 0)

        user2_comment_tweet = self.create_comment(
            user=self.user2,
            tweet=self.user1_tweet,
        )
        NotificationService.send_comment_notification(user2_comment_tweet)
        self.assertEqual(Notification.objects.count(), 1)
