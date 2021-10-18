from newsfeeds.models import NewsFeed
from friendships.models import Friendship
from rest_framework.test import APIClient
from testing.testcases import TestCase


NEWSFEEDS_URL = '/api/newsfeeds/'
POST_TWEETS_URL = '/api/tweets/'
FOLLOW_URL = '/api/friendships/{}/follow/'


class NewsFeedApiTests(TestCase):

    def setUp(self):
        self.test1 = self.create_user('test1')
        self.test1_client = APIClient()
        self.test1_client.force_authenticate(self.test1)

        self.test2 = self.create_user('test2')
        self.test2_client = APIClient()
        self.test2_client.force_authenticate(self.test2)

        # create followings and followers for test1
        for i in range(2):
            follower = self.create_user('test1_follower{}'.format(i))
            Friendship.objects.create(from_user=follower, to_user=self.test1)
        for i in range(3):
            following = self.create_user('test1_following{}'.format(i))
            Friendship.objects.create(from_user=self.test1, to_user=following)

    def test_list(self):
        # 需要登录
        response = self.anonymous_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 403)
        # 不能用 post
        response = self.test1_client.post(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 405)
        # 一开始啥都没有
        response = self.test1_client.get(NEWSFEEDS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Newsfeeds']), 0)
        # 自己发的信息是可以看到的
        self.test1_client.post(POST_TWEETS_URL, {'content': 'Hello World'})
        response = self.test1_client.get(NEWSFEEDS_URL)
        self.assertEqual(len(response.data['Newsfeeds']), 1)
        # 关注之后可以看到别人发的
        self.test1_client.post(FOLLOW_URL.format(self.test2.id))
        response = self.test2_client.post(POST_TWEETS_URL, {
            'content': 'Hello Twitter',
        })
        """
        print(response.data) =>
        {
            'Success': True, 
            'Content': {
                    'id': 7, 
                    'user': OrderedDict([
                                ('id', 41), 
                                ('username', 'test2')
                                ]), 
                    'created_at': '2021-10-18T01:03:43.802169Z', 
                    'content': 'Hello Twitter'
            }
        }
        """
        posted_tweet_id = response.data['Content']['id']
        response = self.test1_client.get(NEWSFEEDS_URL)
        self.assertEqual(len(response.data['Newsfeeds']), 2)
        self.assertEqual(response.data['Newsfeeds'][0]['tweet']['id'], posted_tweet_id)
