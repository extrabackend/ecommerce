from rest_framework import status
from rest_framework.exceptions import APIException


class PhoneNumberNotFoundError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Phone number does not exists'
    default_code = 'phone_number_not_found'


class InvalidCredentialsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'phone number or password is incorrect'
    default_code = 'invalid_credentials'
