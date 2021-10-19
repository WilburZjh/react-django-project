from testing.testcases import TestCase


# Create your tests here.
class CommentModelTest(TestCase):

    def setUp(self):
        self.user=self.create_user('user')
        self.tweet=self.create_tweet(user=self.user)
        self.comment=self.create_comment(user=self.user, tweet=self.tweet)

    def test_comment(self):
        self.assertNotEqual(self.comment.__str__(), None)

    def test_like(self):
        self.create_like(user=self.user, target=self.comment)
        self.assertEqual(self.comment.like_set.count(), 1)

        self.create_like(user=self.user, target=self.comment)
        self.assertEqual(self.comment.like_set.count(), 1)

        user2 = self.create_user('user2')
        self.create_like(user=user2, target=self.comment)
        self.assertEqual(self.comment.like_set.count(), 2)
