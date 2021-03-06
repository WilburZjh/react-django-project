from testing.testcases import TestCase
from comments.models import Comment
from rest_framework.test import APIClient

COMMENT_URL='/api/comments/'
COMMENT_DETAIL_URL='/api/comments/{}/'
TWEET_LIST_API = '/api/tweets/'
TWEET_DETAIL_API = '/api/tweets/{}/'
NEWSFEED_LIST_API = '/api/newsfeeds/'

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
        self.assertEqual(response.status_code, 400)

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
        comment.refresh_from_db() # comment ?????????DB???object????????????????????????model????????????????????????
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

    def test_comments_count(self):
        # test tweet detail api
        tweet = self.create_tweet(self.test1)
        url = TWEET_DETAIL_API.format(tweet.id)
        response = self.test2_client.get(url)
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.assertEqual(response.data['Tweet']['comments_count'], 0)

        # test tweet list api
        self.create_comment(self.test1, tweet)
        response = self.test2_client.get(TWEET_LIST_API, {'user_id': self.test1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Tweets'][0]['comments_count'], 1)

        # test newsfeeds list api
        self.create_comment(self.test2, tweet)
        self.create_newsfeed(self.test2, tweet)
        response = self.test2_client.get(NEWSFEED_LIST_API)
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.assertEqual(response.data['Newsfeeds'][0]['tweet']['comments_count'], 2)
