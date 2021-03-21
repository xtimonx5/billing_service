from django.contrib.auth import get_user_model

from typing import Optional

User = get_user_model()


class UserDAO:
    @classmethod
    def is_allowed_to_receive_transfer(cls, username: str) -> User:
        return User.objects.filter(username=username, is_active=True).exists()

    @classmethod
    def get_user_by_username(cls, username: str) -> Optional[User]:
        return User.objects.filter(username=username, is_active=True).first()
