from testing.testcases import TestCase
from rest_framework.test import APIClient

COMMENT_URL='/api/comments/'

class CommentAPITest(TestCase):

    def setUp(self):
        self.test1 = self.create_user('test1')
        self.test1_client = APIClient()
        self.test1_client.force_authenticate(self.test1)

        self.test2 = self.create_user('test2')
        self.test2_client = APIClient()
        self.test2_client.force_authenticate(self.test2)

        self.tweet1 = self.create_tweet(user=self.test1)


    def test_create(self):
        response = self.anonymous_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 403)

        response = self.test1_client.get(COMMENT_URL)
        self.assertEqual(response.status_code, 405)

        # response = self.test1_client.post(COMMENT_URL)
        # self.assertEqual(response.status_code, 400)

        response = self.test1_client.post(COMMENT_URL, {'tweet_id': self.tweet1.id, 'content': 'Hello World'})
        self.assertEqual(response.status_code, 200)
        print(response.data)
        # {
        #   'Success': True,
        #   'Comment': {
        #       'user': OrderedDict([('id', 1), ('username', 'test1')]),
        #       'tweet': OrderedDict([('id', 1), ('user', OrderedDict([('id', 1), ('username', 'test1')])), ('created_at', '2021-10-17T00:26:19.451343Z'), ('content', 'test content')])}}
        self.assertEqual(response.data['Comment']['user']['username'], 'test1')
        self.assertEqual(response.data['Comment']['user']['id'], self.test1.id)
        self.assertEqual(response.data['Comment']['tweet']['id'], self.tweet1.id)

