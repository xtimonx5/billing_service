from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from oauth2_provider.models import Application

from common.models import UserAccount

User = get_user_model()


class RegisterTestCase(APITestCase):
    registration_url = reverse('register')

    def test_user_registration_with_valid_data(self):
        data = {
            'username': 'TestUser',
            'email': 'example@example.com',
            'password': "123123123qweas"
        }

        response = self.client.post(path=self.registration_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        self.assertEqual(response_data['username'], data['username'])
        self.assertEqual(response_data['email'], data['email'])

        access_token = Application.objects.get(user__username=data['username'])
        self.assertEqual(access_token.client_id, response_data['client_id'])
        self.assertEqual(access_token.client_secret, response_data['client_secret'])
        self.assertTrue(UserAccount.objects.filter(user__username=data['username']).exists())
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_with_invalid_email(self):
        data = {
            'username': 'TestUser',
            'email': 'not_valid_email',
            'password': "123123123qweas"
        }
        response = self.client.post(path=self.registration_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_user_registration_with_not_unique_username(self):
        User.objects.create_user(username='TestUser', email='123@21312.qcom', password='123123123123q')
        data = {
            'username': 'TestUser',
            'email': 'example@example.com',
            'password': "123123123qweas"
        }
        response = self.client.post(path=self.registration_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_with_simple_password(self):
        data = {
            'username': 'TestUser',
            'email': 'example@example.com',
            'password': "1"
        }

        response = self.client.post(path=self.registration_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(User.objects.count(), 0)
