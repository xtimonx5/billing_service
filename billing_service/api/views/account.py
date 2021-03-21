from django.conf import settings
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from common.services.daos import AccountDAO
from api.serializers import AccountSerializer
from common.models import UserAccount


class AccountView(APIView):
    permission_classes = [TokenHasScope, ]

    required_scopes = [settings.ACCOUNT_SCOPE, ]

    def get_object(self) -> UserAccount:
        return AccountDAO.get_account_by_user(user=self.request.user, prefetch_history=True)

    def get_serializer(self, *args, **kwargs) -> AccountSerializer:
        return AccountSerializer(instance=self.get_object())

    def get(self, request: Request) -> Response:
        serializer = self.get_serializer()
        return Response(serializer.data)
