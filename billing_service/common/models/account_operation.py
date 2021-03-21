from django.utils.translation import ugettext_lazy as _
from django.db import models

import common.constants

from .mixins import CreatedModelMixin


class AccountOperation(CreatedModelMixin, models.Model):
    DEPOSIT_OPERATION = common.constants.OPERATION_DEPOSIT
    TRANSFER_OPERATION = common.constants.OPERATION_TRANSFER
    OPERATION_TYPE_CHOICES = (
        (common.constants.OPERATION_DEPOSIT, _('Deposit')),
        (common.constants.OPERATION_TRANSFER, _('Transfer')),
    )
    account = models.ForeignKey(
        'common.UserAccount',
        on_delete=models.CASCADE,
        db_index=False,
        related_name='operations'
    )
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPE_CHOICES, blank=False, null=False)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )

    class Meta:
        index_together = [
            ('account', 'created')
        ]
