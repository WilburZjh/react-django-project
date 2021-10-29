from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet, TweetPhoto
from django.core.files.uploadedfile import SimpleUploadedFile


TWEET_LIST_URL = '/api/tweets/'
TWEET_CREATE_URL = '/api/tweets/'
TWEET_RETRIEVE_URL = '/api/tweets/{}/'

class TweetTestCase(TestCase):

    def setUp(self):

        self.user1 = self.create_user(username='user1')
        self.tweet1 = [
            self.create_tweet(
                user = self.user1,
            )
            for _ in range(3)
        ]

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1) #

        self.user2 = self.create_user(username = 'user2')
        self.tweet2 = [
            self.create_tweet(
                user = self.user2,
            )
            for _ in range(2)
        ]

    def test_list(self):
        response = self.anonymous_client.get(path=TWEET_LIST_URL)
        self.assertEqual(response.status_code, 400)

        response = self.anonymous_client.get(TWEET_LIST_URL, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Tweets']), 3)

        response = self.anonymous_client.get(path=TWEET_LIST_URL, data={'user_id': self.user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Tweets']), 2)

        self.assertEqual(response.data['Tweets'][0]['id'], self.tweet2[1].id)
        self.assertEqual(response.data['Tweets'][1]['id'], self.tweet2[0].id)

    def test_create(self):
        response = self.anonymous_client.post(TWEET_CREATE_URL)
        self.assertEqual(response.status_code, 403)

        # 必须带 content
        response = self.user1_client.post(TWEET_CREATE_URL)
        self.assertEqual(response.status_code, 400)
        # content 不能太短
        response = self.user1_client.post(TWEET_CREATE_URL, {'content': '1'})
        self.assertEqual(response.status_code, 400)
        # content 不能太长
        response = self.user1_client.post(TWEET_CREATE_URL, {
            'content': '0' * 141
        })
        self.assertEqual(response.status_code, 400)

        # 正常发帖
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_URL, {
            'content': 'Hello World, this is my first tweet!'
        })
        self.assertEqual(response.status_code, 201)
        # print(response.data)
        self.assertEqual(response.data['Content']['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)

    def test_create_with_files(self):
        response = self.user1_client.post(TWEET_CREATE_URL, {
            'content': 'a selfie',
            'files': [],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TweetPhoto.objects.count(), 0)

        # 上传单个文件
        # content 需要是一个 bytes 类型，所以用 str.encode 转换一下
        file = SimpleUploadedFile(
            name='selfie.jpg',
            content=str.encode('a fake image'),
            content_type='image/jpeg',
        )
        response = self.user1_client.post(TWEET_CREATE_URL, {
            'content': 'a selfie',
            'files': [file],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TweetPhoto.objects.count(), 1)

        # 测试多个文件上传
        file1 = SimpleUploadedFile(
            name='selfie1.jpg',
            content=str.encode('selfie 1'),
            content_type='image/jpeg',
        )
        file2 = SimpleUploadedFile(
            name='selfie2.jpg',
            content=str.encode('selfie 2'),
            content_type='image/jpeg',
        )
        response = self.user1_client.post(TWEET_CREATE_URL, {
            'content': 'two selfies',
            'files': [file1, file2],
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TweetPhoto.objects.count(), 3)

        # 从读取的 API 里确保已经包含了 photo 的地址
        retrieve_url = TWEET_RETRIEVE_URL.format(response.data['Content']['id'])
        response = self.user1_client.get(retrieve_url)
        print(response.data)
        self.assertEqual(len(response.data['Tweet']['photo_urls']), 2)
        self.assertEqual('selfie1' in response.data['Tweet']['photo_urls'][0], True)
        self.assertEqual('selfie2' in response.data['Tweet']['photo_urls'][1], True)

        # 测试上传超过 9 个文件会失败
        files = [
            SimpleUploadedFile(
                name=f'selfie{i}.jpg',
                content=str.encode(f'selfie{i}'),
                content_type='image/jpeg',
            )
            for i in range(10)
        ]
        response = self.user1_client.post(TWEET_CREATE_URL, {
            'content': 'failed due to number of photos exceeded limit',
            'files': files,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TweetPhoto.objects.count(), 3)

    def test_retrieve(self):
        response = self.anonymous_client.get(TWEET_LIST_URL)
        self.assertEqual(response.status_code, 400)

        response = self.anonymous_client.get(TWEET_RETRIEVE_URL.format(-1))
        self.assertEqual(response.status_code, 404)

        tweet = self.create_tweet(self.user1)
        response = self.anonymous_client.get(TWEET_RETRIEVE_URL.format(tweet.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Tweet']['comments']), 0)

        comment1 = self.create_comment(self.user1, tweet, 'user1 comment on tweet.')
        comment2 = self.create_comment(self.user2, tweet, 'user2 comment on tweet.')
        response = self.anonymous_client.get(TWEET_RETRIEVE_URL.format(tweet.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['Tweet']['comments']), 2)

        profile = self.user1.profile
        self.assertEqual(response.data['Tweet']['user']['nickname'], profile.nickname)
        self.assertEqual(response.data['Tweet']['user']['avatar_url'], None)
