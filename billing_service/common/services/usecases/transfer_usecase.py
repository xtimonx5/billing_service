from django.db.transaction import atomic

from common.models import AccountOperation
from common.services.daos import AccountDAO
from common.models import UserAccount
import common.constants


class TransferUseCase:
    def __init__(self, sender, recipient, amount):
        self._sender = sender
        self._recipient = recipient
        self._amount = amount

    @atomic
    def _perform_transfer(self, recipient_account: UserAccount, sender_account: UserAccount):
        recipient_account.balance += self._amount
        sender_account.balance -= self._amount

        recipient_account.save()
        sender_account.save()

        AccountOperation.objects.create(
            account=recipient_account,
            operation_type=common.constants.OPERATION_TRANSFER,
            amount=self._amount
        )
        AccountOperation.objects.create(
            account=sender_account,
            operation_type=common.constants.OPERATION_TRANSFER,
            amount=self._amount * -1
        )

    def execute(self):
        sender_account = AccountDAO.get_account_by_user(self._sender)
        recipient_account = AccountDAO.get_account_by_user(self._recipient)
        self._perform_transfer(
            recipient_account=recipient_account,
            sender_account=sender_account
        )
