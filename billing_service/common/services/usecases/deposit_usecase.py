from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from common.models import UserAccount, AccountOperation
from common.services.daos import AccountDAO

import common.constants

User = get_user_model()


class DepositUseCase:
    def __init__(self, user: User, amount: Decimal) -> None:
        self._user = user
        self._amount = amount

    def _get_account(self) -> UserAccount:
        return AccountDAO.get_account_by_user(user=self._user)

    @atomic
    def _deposit_to_account(self, account: UserAccount, amount: Decimal) -> UserAccount:
        account.balance += amount
        account.save()
        AccountOperation.objects.create(
            account=account,
            operation_type=common.constants.OPERATION_DEPOSIT,
            amount=amount
        )
        return account

    def execute(self) -> UserAccount:
        account = self._get_account()
        self._deposit_to_account(account, self._amount)

        return account
