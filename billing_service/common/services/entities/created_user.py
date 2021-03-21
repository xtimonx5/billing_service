import base64


class CreatedUserEntity:
    def __init__(self, username: str, email: str, client_id: str, client_secret: str) -> None:
        self._username = username
        self._email = email
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_secret(self) -> str:
        return self._client_secret

    @property
    def b64header(self) -> str:
        credential = "{0}:{1}".format(self.client_id, self.client_secret)
        return base64.b64encode(credential.encode("utf-8")).decode()
