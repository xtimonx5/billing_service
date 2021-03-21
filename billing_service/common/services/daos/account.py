from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from common.models import UserAccount, AccountOperation

User = get_user_model()


class AccountDAO:
    @classmethod
    def get_account_by_user(cls, user: User, prefetch_history: bool = False) -> UserAccount:
        user_qs = UserAccount.objects.filter(user=user)
        if prefetch_history:
            history_prefetch = Prefetch(
                lookup='operations',
                queryset=AccountOperation.objects.order_by('-created'),
                to_attr='history'
            )
            user_qs = user_qs.select_related('user').prefetch_related(history_prefetch)

        return user_qs.first()
