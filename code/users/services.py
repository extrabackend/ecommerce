from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import APIException

from . import repositores, constants


User = get_user_model()


class UserService:

    def __init__(self, repository: repositores.UserRepository = repositores.UserRepository()):
        self.repository = repository

    def create_user(self, data: dict) -> User:
        session_key = constants.USER_SESSION_KEY.format(data['session_id'])
        session = cache.get(session_key)

        if session is None:
            raise APIException('session is expired', status.HTTP_500_INTERNAL_SERVER_ERROR)

        code = session.pop('code')

        if code != data['code']:
            raise APIException('sms code is invalid', status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = self.repository.create_user(session)
        cache.delete(session_key)

        return user
