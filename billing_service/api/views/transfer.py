from django.conf import settings
from oauth2_provider.contrib.rest_framework import TokenHasScope

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from api.serializers import TransferSerializer
from common.services.usecases import TransferUseCase


class TransferView(views.APIView):
    permission_classes = [TokenHasScope, ]

    required_scopes = [settings.TRANSFER_SCOPE, ]

    def _perform_transfer(self, validated_data: dict) -> None:
        recipient = validated_data['recipient_username']
        sender = self.request.user
        amount = validated_data['amount']
        TransferUseCase(
            recipient=recipient,
            sender=sender,
            amount=amount
        ).execute()

    def _get_serializer(self) -> TransferSerializer:
        return TransferSerializer(
            data=self.request.data,
            context={'request': self.request}
        )

    def post(self, request: Request) -> Response:
        serializer = self._get_serializer()
        if serializer.is_valid():
            self._perform_transfer(serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
