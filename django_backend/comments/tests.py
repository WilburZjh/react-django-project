from testing.testcases import TestCase

# Create your tests here.
class CommentModelTest(TestCase):

    def test_comment(self):
        self.user=self.create_user('test1')
        self.tweet=self.create_tweet(user=self.user)
        self.comment=self.create_comment(user=self.user, tweet=self.tweet)
        self.assertNotEqual(self.comment.__str__(), None)
