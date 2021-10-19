from testing.testcases import TestCase
from datetime import timedelta
from utils.time_helpers import utc_now

# Create your tests here.
class TweetTest(TestCase):

    def setUp(self):
        self.user = self.create_user('user')
        self.tweet = self.create_tweet(user=self.user)


    def test_hour_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=10)
        self.tweet.save()
        self.assertEqual(self.tweet.hours_to_now(), 10)

    def test_tweet_like(self):
        self.create_like(user=self.user, target=self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        self.create_like(user=self.user, target=self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        user2 = self.create_user('user2')
        self.create_like(user=user2, target=self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)
