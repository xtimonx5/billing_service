from decimal import Decimal

from rest_framework import serializers

from common.services.daos import UserDAO, AccountDAO


class TransferSerializer(serializers.Serializer):
    recipient_username = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))

    def validate_recipient_username(self, value: str):
        user = UserDAO.get_user_by_username(value)
        if not user:
            raise serializers.ValidationError("User does not exist")
        if user.pk == self.context['request'].user.pk:
            raise serializers.ValidationError("You can not transfer money to yourself")
        return user

    def validate_amount(self, value: Decimal) -> Decimal:
        sender = self.context['request'].user
        account = AccountDAO.get_account_by_user(sender)
        if account.balance < value:
            raise serializers.ValidationError("Insufficient balance to perform transfer")
        return value
