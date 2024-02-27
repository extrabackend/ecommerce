from django.contrib.auth import get_user_model


User = get_user_model()


class UserRepository:

    def create_user(self, data: dict) -> User:
        return User.objects.create_user(**data)

    def get_user(self, **kwargs) -> User:
        return User.objects.get(**kwargs)
