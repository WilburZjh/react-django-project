from accounts.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from testing.testcases import TestCase


LOGIN_URL = '/api/accounts/login/'
CHECK_STATUS_URL = '/api/accounts/check_status/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
USER_PROFILE_DETAIL_URL = '/api/profiles/{}/'


class AccountAPITest(TestCase):

    def setUp(self):
        # 这个函数会在每个 test function 执行的时候被执行
        self.client = APIClient()
        self.user = self.create_user(
            username='test',
            password='test',
            email='test@reactdjango.com'
        )

    def test_login(self):
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test',
        })
        self.assertEqual(response.status_code, 405)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(LOGIN_URL, {
            'username': 'wrong username',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.get(CHECK_STATUS_URL)
        # print(response)
        self.assertEqual(response.data['Has_logged_in'], False)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['User'], None)
        self.assertEqual(response.data['User']['id'], self.user.id)

        response = self.client.get(CHECK_STATUS_URL)
        self.assertEqual(response.data['Has_logged_in'], True)


    def test_logout(self):
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test',
        })
        response = self.client.get(CHECK_STATUS_URL)
        self.assertEqual(response.data['Has_logged_in'], True)

        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(LOGOUT_URL,{})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Logged out'], True)

        response = self.client.get(CHECK_STATUS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Has_logged_in'], False)

    def test_signup(self):
        new_user = {
            'username': 'someone',
            'password': 'password',
            'email': 'someone@reactdjango.com',
        }
        response = self.client.get(SIGNUP_URL, new_user)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'password': 'password',
            'email': 'not a valid email address',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'password': '888888888888888888888888888888888888888888888888888',
            'email': 'someone@reactdjango.com',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(SIGNUP_URL, {
            'username': 'someonesomeonesomeone someonesomeonesomeone',
            'password': 'password',
            'email': 'someone@reactdjango.com',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(SIGNUP_URL, new_user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['User']['username'], 'someone')

        # 验证 user profile 已经被创建
        created_user_id = response.data['User']['id']
        profile = UserProfile.objects.filter(user_id=created_user_id).first()
        self.assertNotEqual(profile, None)

        response = self.client.get(CHECK_STATUS_URL)
        self.assertEqual(response.data['Has_logged_in'], True)

class UserProfileAPITest(TestCase):

    def setUp(self):
        self.user1, self.user1_client = self.create_user_and_client('user1')
        self.user2, self.user2_client = self.create_user_and_client('user2')

    def test_update(self):
        p = self.user1.profile
        p.nickname = 'old nickname'
        p.save()
        url = USER_PROFILE_DETAIL_URL.format(p.id)

        response = self.user2_client.put(url, {
            'nickname': 'a new nickname',
        })
        self.assertEqual(response.status_code, 403)
        p.refresh_from_db()
        self.assertEqual(p.nickname, 'old nickname')

        response = self.user1_client.put(url, {
            'nickname': 'a new nickname',
        })
        self.assertEqual(response.status_code, 200)
        p.refresh_from_db()
        self.assertEqual(p.nickname, 'a new nickname')

        response = self.user1_client.put(url, {
            'avatar': SimpleUploadedFile(
                name='my-avatar.jpg',
                content=str.encode('a fake image'),
                content_type='image/jpeg',
            ),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual('my-avatar' in response.data['avatar'], True)
        p.refresh_from_db()
        self.assertIsNotNone(p.avatar)
