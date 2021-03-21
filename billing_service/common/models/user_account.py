from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from .mixins import CreatedModelMixin


class UserAccount(CreatedModelMixin, models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0'))],
        default=Decimal('0')
    )

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte=Decimal('0')), name='balance_gte_0'),
        ]
