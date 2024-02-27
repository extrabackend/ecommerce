import random
import uuid

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.tokens import RefreshToken

from . import constants, serializers, exceptions, services


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    service: services.UserService = services.UserService()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUserSerializer

        if self.action == 'session':
            return serializers.CreateUserSessionSerializer

        if self.action == 'create_token':
            return serializers.CreateTokenSerializer

        if self.action == 'refresh_token':
            return serializers.RefreshTokenSerializer

        return serializers.UserSerializer

    @action(detail=False, url_path='session', methods=['POST'])
    def session(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = uuid.uuid4()
        sms_code = self._generate_sms_code()  # 0012
        print('sms code:', sms_code)

        cache.set(
            constants.USER_SESSION_KEY.format(session_id),
            {**serializer.validated_data, 'code': sms_code},
            constants.USER_SESSION_KEY_TTL,
        )

        return Response({'session_id': session_id})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.service.create_user(data=serializer.validated_data)
        serializer = serializers.UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _generate_sms_code(self):
        numbers = '0123456789'
        # send sms to client
        return ''.join(random.choices(numbers, k=4))

    @action(detail=False, url_path='logon', methods=('POST',))
    def create_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        users = User.objects.filter(phone_number=serializer.validated_data['phone_number'])

        if not users.exists():
            raise exceptions.PhoneNumberNotFoundError

        user = users.first()

        if not user.check_password(serializer.validated_data['password']):
            raise exceptions.InvalidCredentialsError

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, url_path='refresh', methods=('POST',))
    def refresh_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = RefreshToken(serializer.validated_data['refresh'])
        refresh.set_exp()
        refresh.set_iat()

        return Response({
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# 1. Enter phone_number, email and password
# 2. create unique key {..., sms: '4444'}
# 3. Send sms and send key to response
# 4. send back key and sms and verification
# 5. create user

