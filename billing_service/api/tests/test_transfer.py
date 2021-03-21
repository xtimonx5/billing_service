from datetime import datetime

from oauth2_provider.models import AccessToken

from common.models import UserAccount, AccountOperation
from .base_api_test import BaseApiTestCase
from rest_framework.reverse import reverse
from rest_framework import status


class TransferTestCase(BaseApiTestCase):
    required_scope = 'transfer'
    url = reverse('transfer')

    def setUp(self) -> None:
        super(TransferTestCase, self).setUp()
        _, self.recipient_account = self._create_user_and_account(username='mr.recipient')
        self.user_account.balance = 1000
        self.user_account.save()

    def test_transfer_with_valid_data(self):
        data = {
            'recipient_username': 'mr.recipient',
            'amount': 10
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sender_account = UserAccount.objects.get(pk=self.user_account.pk)
        self.assertEqual(sender_account.balance, 990)
        self.assertEqual(AccountOperation.objects.count(), 2)
        recipient_account = UserAccount.objects.get(pk=self.recipient_account.pk)
        self.assertEqual(recipient_account.balance, 10)

        self.assertEqual(recipient_account.operations.count(), 1)
        self.assertEqual(sender_account.operations.count(), 1)

        recipient_operation = recipient_account.operations.first()
        self.assertEqual(recipient_operation.operation_type, AccountOperation.TRANSFER_OPERATION)
        self.assertEqual(recipient_operation.amount, 10)

        sender_operation = sender_account.operations.first()
        self.assertEqual(sender_operation.operation_type, AccountOperation.TRANSFER_OPERATION)
        self.assertEqual(sender_operation.amount, -10)

    def test_transfer_with_insufficient_balance(self):
        data = {
            'recipient_username': 'mr.recipient',
            'amount': 10000
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        sender_account = UserAccount.objects.get(pk=self.user_account.pk)
        self.assertEqual(sender_account.balance, 1000)
        self.assertEqual(AccountOperation.objects.count(), 0)
        recipient_account = UserAccount.objects.get(pk=self.recipient_account.pk)
        self.assertEqual(recipient_account.balance, 0)

    def test_transfer_with_non_existent_recipient(self):
        data = {
            'recipient_username': 'mr.recipient222',
            'amount': 10
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        sender_account = UserAccount.objects.get(pk=self.user_account.pk)
        self.assertEqual(sender_account.balance, 1000)
        self.assertEqual(AccountOperation.objects.count(), 0)
        recipient_account = UserAccount.objects.get(pk=self.recipient_account.pk)
        self.assertEqual(recipient_account.balance, 0)

    def test_transfer_to_yourself(self):
        data = {
            'recipient_username': self.user.username,
            'amount': 10
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        sender_account = UserAccount.objects.get(pk=self.user_account.pk)
        self.assertEqual(sender_account.balance, 1000)
        self.assertEqual(AccountOperation.objects.count(), 0)
        recipient_account = UserAccount.objects.get(pk=self.recipient_account.pk)
        self.assertEqual(recipient_account.balance, 0)

    def test_transfer_without_headers(self):
        data = {
            'recipient_username': 'mr.recipient',
            'amount': 10
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        sender_account = UserAccount.objects.get(pk=self.user_account.pk)
        self.assertEqual(sender_account.balance, 1000)
        self.assertEqual(AccountOperation.objects.count(), 0)

    def test_transfer_with_invalid_scope(self):
        deposit_access_token = AccessToken.objects.create(
            token='new_token',
            scope='deposit',
            user=self.user,
            expires=datetime.max
        )
        data = {
            'recipient_username': 'mr.recipient',
            'amount': 10
        }
        response = self.client.post(
            path=self.url, data=data, format='json',
            HTTP_AUTHORIZATION='Bearer {}'.format(deposit_access_token.token)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        sender_account = UserAccount.objects.get(pk=self.user_account.pk)
        self.assertEqual(sender_account.balance, 1000)
        self.assertEqual(AccountOperation.objects.count(), 0)
