from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    client_id = serializers.CharField(read_only=True)
    client_secret = serializers.CharField(read_only=True)
    b64header = serializers.CharField(read_only=True)

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def validate_username(self, value: str) -> User:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('User with such username already exists')
        return value
