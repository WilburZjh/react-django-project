from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


LOGIN_URL = '/api/accounts/login/'
CHECK_STATUS_URL = '/api/accounts/check_status/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'

class AccountAPITest(TestCase):

    def setUp(self):
        # 这个函数会在每个 test function 执行的时候被执行
        self.client = APIClient()
        self.user = self.createUser(
            username='test',
            password='test',
            email='test@reactdjango.com'
        )

    def createUser(self, username, password, email):
        return User.objects.create_user(username=username, password=password, email=email)

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
        print(response)
        self.assertEqual(response.data['Has_logged_in'], False)

        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'test',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['User'], None)
        self.assertEqual(response.data['User']['email'], 'test@reactdjango.com')

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['User']['username'], 'someone')

        response = self.client.get(CHECK_STATUS_URL)
        self.assertEqual(response.data['Has_logged_in'], True)
