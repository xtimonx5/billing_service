from datetime import datetime

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken

from common.models import UserAccount

User = get_user_model()


class BaseApiTestCase(APITestCase):
    required_scope = ''
    url = ''

    def _create_user_and_account(self, username='TestUser'):
        user = User.objects.create_user(username=username, email='123@21312.qcom', password='123123123123q')
        user_account = UserAccount.objects.create(user=user)
        return user, user_account

    def _create_api_access_token(self):
        Application.objects.create(
            user=self.user,
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )
        access_token = AccessToken.objects.create(
            token='test_tokentest_token',
            scope=self.required_scope,
            user=self.user,
            expires=datetime.max
        )
        return access_token.token

    def setUp(self) -> None:
        self.user, self.user_account = self._create_user_and_account()
        token = self._create_api_access_token()
        self.auth_header = 'Bearer {}'.format(token)
