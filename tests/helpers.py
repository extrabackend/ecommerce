import json

from django.contrib.auth import get_user_model


User = get_user_model()


def load_json_data(path: str):
    with open(f'tests/data/{path}') as file:
        return json.load(file)


class UserRepositoryMock:

    def create_user(self, data):
        return User(**data)
