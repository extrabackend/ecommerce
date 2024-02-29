import pytest
from django.db import IntegrityError

from helpers import load_json_data

from users.repositores import UserRepository


@pytest.mark.django_db
class TestUserRepository:
    repository = UserRepository()

    @pytest.fixture(autouse=True)
    def load_fixtures(self, load_data):
        load_data('users.json')

    def test_create_user_base(self):
        data = load_json_data('users/repositories/create_user/base/payload.json')
        user = self.repository.create_user(data)

        assert user.phone_number == data['phone_number']
        assert user.email == data['email']
        assert user.check_password(data['password'])

    def test_create_user_failure(self):
        data = load_json_data(
            'users/repositories/create_user/phone_number_already_exists/payload.json',
        )

        with pytest.raises(IntegrityError):
            self.repository.create_user(data)
