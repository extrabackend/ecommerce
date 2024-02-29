import uuid

import pytest

from django.core.cache import cache
from rest_framework.exceptions import APIException

from helpers import load_json_data

from users import constants, utils
from users.services import UserService


class TestUserService:

    def test_create_user(self, repository):
        payload = load_json_data('users/services/create_user/base/payload.json')
        session = load_json_data('users/services/create_user/base/session.json')

        session_key = constants.USER_SESSION_KEY.format(payload['session_id'])
        cache.set(session_key, session, constants.USER_SESSION_KEY_TTL)

        service = UserService(repository)

        user = service.create_user(payload)

        assert user.email == session['email']
        assert user.phone_number == session['phone_number']
        assert session_key not in cache

    def test_create_user_session_expired(self, repository):
        payload = load_json_data('users/services/create_user/base/payload.json')
        service = UserService(repository)

        with pytest.raises(APIException):
            service.create_user(payload)

    def test_create_user_invalid_sms(self, repository):
        payload = load_json_data('users/services/create_user/invalid_code/payload.json')
        session = load_json_data('users/services/create_user/invalid_code/session.json')

        session_key = constants.USER_SESSION_KEY.format(payload['session_id'])
        cache.set(
            session_key,
            session,
            constants.USER_SESSION_KEY_TTL,
        )
        service = UserService(repository)

        with pytest.raises(APIException):
            service.create_user(payload)


def test_generate_uuid(mocker):
    mocker.patch('uuid.uuid4', return_value=uuid.UUID('8211ce0b-acf0-4b47-be6a-6b70571a6d04'))
    assert uuid.UUID('8211ce0b-acf0-4b47-be6a-6b70571a6d04') == utils.generate_uuid()
