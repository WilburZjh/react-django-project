from testing.testcases import TestCase
from rest_framework.test import APIClient
from friendships.models import Friendship

FOLLOW_URL = '/api/friendships/{}/follow/'
UNFOLLOW_URL = '/api/friendships/{}/unfollow/'
FOLLOWERS_URL = '/api/friendships/{}/followers/'
FOLLOWINGS_URL = '/api/friendships/{}/followings/'

class FrienshipAPITest(TestCase):

    def setUp(self):
        self.anonymous_client = APIClient()

        self.test1 = self.create_user(username='test1')
        self.test1_client = APIClient()
        self.test1_client.force_authenticate(self.test1)

        self.test2 = self.create_user(username='test2')
        self.test2_client = APIClient()
        self.test2_client.force_authenticate(self.test2)

        for i in range(2):
            follower = self.create_user('test1_follower_{}'.format(i))
            Friendship.objects.create(from_user=follower, to_user=self.test1)

        for i in range(3):
            following = self.create_user('test1_following_{}'.format(i))
            Friendship.objects.create(from_user=self.test1, to_user=following)

    def test_follower(self):
        url = FOLLOWERS_URL.format(self.test1.id)

        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, 405)

        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Followers']), 2)

        ts0 = response.data['Followers'][0]['created_at']
        ts1 = response.data['Followers'][1]['created_at']
        print(ts0, ts1)
        self.assertEqual(ts0 > ts1, True)

        print(response.data)
        self.assertEqual(response.data['Followers'][0]['user']['username'], 'test1_follower_1')
        self.assertEqual(response.data['Followers'][1]['user']['username'], 'test1_follower_0')

    def test_following(self):
        url = FOLLOWINGS_URL.format(self.test1.id)

        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, 405)

        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Followings']), 3)

        # 确保按照时间倒序
        ts0 = response.data['Followings'][0]['created_at']
        ts1 = response.data['Followings'][1]['created_at']
        ts2 = response.data['Followings'][2]['created_at']
        self.assertEqual(ts0 > ts1, True)
        self.assertEqual(ts1 > ts2, True)
        self.assertEqual(
            response.data['Followings'][0]['user']['username'],
            'test1_following_2',
        )
        self.assertEqual(
            response.data['Followings'][1]['user']['username'],
            'test1_following_1',
        )
        self.assertEqual(
            response.data['Followings'][2]['user']['username'],
            'test1_following_0',
        )

    def test_follow(self):
        url = FOLLOW_URL.format(self.test2.id)

        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, 403)

        response = self.test1_client.get(url)
        self.assertEqual(response.status_code, 405)

        response = self.test2_client.post(url)
        self.assertEqual(response.status_code, 400)

        response = self.test1_client.post(url)
        self.assertEqual(response.status_code, 200)

        response = self.test1_client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['Duplicate'], True)

        response = self.anonymous_client.get(FOLLOWERS_URL.format(self.test2.id))
        self.assertEqual(len(response.data['Followers']), 1)


    def test_unfollow(self):
        url = UNFOLLOW_URL.format(self.test2.id)

        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, 403)

        response = self.test1_client.get(url)
        self.assertEqual(response.status_code, 405)

        Friendship.objects.create(from_user=self.test1, to_user=self.test2)
        count = Friendship.objects.count()
        response = self.test1_client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.count(), count-1)

        count = Friendship.objects.count()
        response = self.test1_client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.count(), count)
