import pytest

from django.core.cache import cache
from rest_framework.exceptions import APIException

from helpers import load_json_data, UserRepositoryMock

from users import constants
from users.services import UserService


class TestUserService:
    service = UserService(repository=UserRepositoryMock())

    def test_create_user(self):
        payload = load_json_data('users/services/create_user/base/payload.json')
        session = load_json_data('users/services/create_user/base/session.json')

        session_key = constants.USER_SESSION_KEY.format(payload['session_id'])
        cache.set(session_key, session, constants.USER_SESSION_KEY_TTL)

        user = self.service.create_user(payload)

        assert user.email == session['email']
        assert user.phone_number == session['phone_number']
        assert session_key not in cache

    def test_create_user_session_expired(self):
        payload = load_json_data('users/services/create_user/base/payload.json')

        with pytest.raises(APIException):
            self.service.create_user(payload)

    def test_create_user_invalid_sms(self):
        payload = load_json_data('users/services/create_user/invalid_code/payload.json')
        session = load_json_data('users/services/create_user/invalid_code/session.json')

        session_key = constants.USER_SESSION_KEY.format(payload['session_id'])
        cache.set(session_key, session, constants.USER_SESSION_KEY_TTL)

        with pytest.raises(APIException):
            self.service.create_user(payload)
