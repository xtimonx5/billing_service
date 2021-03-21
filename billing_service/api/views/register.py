from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework import response
from rest_framework import status
from rest_framework.request import Request
from api.serializers import RegistrationSerializer

from common.services.usecases import UserRegistrationUseCase
from common.services.entities import CreatedUserEntity


class RegistrationView(views.APIView):
    permission_classes = [AllowAny, ]

    def _perform_user_registration(self, user_data: dict) -> CreatedUserEntity:
        created_user = UserRegistrationUseCase(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
        ).execute()
        return created_user

    def post(self, request: Request) -> response.Response:
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = self._perform_user_registration(serializer.validated_data)
            response_data = RegistrationSerializer(user).data

            return response.Response(status=status.HTTP_201_CREATED, data=response_data)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
