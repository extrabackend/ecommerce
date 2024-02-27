import uuid
import random

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _


User = get_user_model()


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=8, unique=True, verbose_name=_('number'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_number(cls) -> str:
        number = ''.join(random.choices('0123456789', k=8))

        if not cls.objects.filter(number=number).exists():
            return number

        return cls.generate_number()

    class Meta:
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    price = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Товары заказа'

# Database relations:
# One to One = Husband and Wife
# One to Many = Mother and Children

