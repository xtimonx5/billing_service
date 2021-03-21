from rest_framework import serializers
from common.models import UserAccount, AccountOperation


class AccountOperationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created')

    class Meta:
        model = AccountOperation
        fields = (
            'date',
            'operation_type',
            'amount',
        )


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    def get_history(self, obj: UserAccount) -> dict:
        return AccountOperationSerializer(obj.history, many=True).data

    def get_username(self, obj: UserAccount) -> str:
        return obj.user.username

    class Meta:
        model = UserAccount
        fields = (
            'balance',
            'username',
            'history'
        )
