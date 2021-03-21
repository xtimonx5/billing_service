from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from oauth2_provider.models import Application

from common.models import UserAccount
from common.services.entities import CreatedUserEntity


User = get_user_model()


class UserRegistrationUseCase:
    GENERATED_PASSWORD_LENGTH = 16

    def __init__(self, username: str, email: str, password: str) -> None:
        self._username = username
        self._email = email
        self._password = password

    def _create_user(self) -> User:
        return User.objects.create_user(
            username=self._username,
            email=self._email,
            password=self._password
        )

    def _create_user_account(self, user: User) -> None:
        UserAccount.objects.create(user=user)

    def _create_api_application(self, user: User) -> Application:
        return Application.objects.create(
            user=user,
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )

    @atomic
    def execute(self) -> CreatedUserEntity:
        user_instance = self._create_user()
        api_application = self._create_api_application(user_instance)
        self._create_user_account(user_instance)

        created_user = CreatedUserEntity(
            username=user_instance.username,
            email=user_instance.email,
            client_id=api_application.client_id,
            client_secret=api_application.client_secret
        )
        return created_user
