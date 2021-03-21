from datetime import datetime

from oauth2_provider.models import AccessToken
from rest_framework.reverse import reverse
from rest_framework import status
import random
from .base_api_test import BaseApiTestCase
from common.models import AccountOperation


class AccountTestCase(BaseApiTestCase):
    url = reverse('account')
    required_scope = 'account'

    def setUp(self) -> None:
        super(AccountTestCase, self).setUp()
        self.user_account.balance = 1000
        self.user_account.save()

    def test_get_account_balance(self):
        response = self.client.get(
            path=self.url,
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'balance': '1000.00',
                'username': self.user.username,
                'history': []
            }
        )

    def test_get_account_balance_with_history(self):
        for x in range(10):
            AccountOperation.objects.create(
                operation_type=random.choice([AccountOperation.DEPOSIT_OPERATION, AccountOperation.TRANSFER_OPERATION]),
                amount=random.randint(1, 100),
                account=self.user_account
            )
        response = self.client.get(
            path=self.url,
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['history']), 10)

    def test_get_account_data_without_token(self):
        response = self.client.get(
            path=self.url,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_account_data_with_invalid_scope(self):
        transfer_access_token = AccessToken.objects.create(
            token='new_token',
            scope='transfer',
            user=self.user,
            expires=datetime.max
        )
        response = self.client.get(
            path=self.url,
            HTTP_AUTHORIZATION='Bearer {}'.format(transfer_access_token.token)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
