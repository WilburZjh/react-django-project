from testing.testcases import TestCase
from comments.models import Comment
from rest_framework.test import APIClient

COMMENT_URL='/api/comments/'
COMMENT_DETAIL_URL='/api/comments/{}/'

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
        # print(response.data)
        """
        print(response.data) =>
        {
            'Success': True, 
            'Comment': {
                'id': 1, 
                'user': OrderedDict([
                            ('id', 1), 
                            ('username', 'test1')
                        ]), 
                'tweet_id': 1, 
                'content': 'Hello World', 
                'created_at': '2021-10-18T00:10:50.211590Z'
            }
        }
        """
        self.assertEqual(response.data['Comment']['user']['username'], 'test1')
        self.assertEqual(response.data['Comment']['user']['id'], self.test1.id)
        self.assertEqual(response.data['Comment']['tweet_id'], self.tweet1.id)

    def test_update(self):
        comment = self.create_comment(self.test1, self.tweet1, 'original')
        another_tweet = self.create_tweet(self.test2)
        url = COMMENT_DETAIL_URL.format(comment.id)

        response = self.anonymous_client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 403)

        response = self.test2_client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 403)
        comment.refresh_from_db() # comment 是一个DB的object，里面的属性就是model定义的时候的属性
        self.assertNotEqual(comment.content, 'new')

        response = self.test1_client.put(url, {'content': 'new'})
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(response.data['Updated comment']['content'], 'new')
        self.assertEqual(comment.content, 'new')

    def test_destroy(self):
        comment = self.create_comment(self.test1, self.tweet1, 'origin')
        url = COMMENT_DETAIL_URL.format(comment.id)

        response = self.anonymous_client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.test2_client.delete(url)
        self.assertEqual(response.status_code, 403)

        count = Comment.objects.count()
        response = self.test1_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), count - 1)
