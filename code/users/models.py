import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):

    def _create_user(self, phone_number, email, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True, null=True)

    USERNAME_FIELD = 'phone_number'
    objects = CustomUserManager()


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name_kz = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name_ru = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name_en = models.CharField(max_length=255, unique=True, blank=True, null=True)
    iso_code = models.CharField(max_length=2, db_index=True, blank=True, null=True)


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name_kz = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name_ru = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name_en = models.CharField(max_length=255, unique=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')
    district = models.CharField(max_length=255)


class AddressAnalytics(models.Model):
    user_id = models.UUIDField()
    city_name = models.CharField()
    country_name = models.CharField()
