from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CreateUserSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password')


class CreateUserSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=4)


class CreateTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
