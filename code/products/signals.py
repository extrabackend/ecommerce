from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.Product)
def my_handler(instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_send = async_to_sync(channel_layer.group_send)
        group_name = 'new-products'
        event = {
            'type': 'new.product.created',
            'action': 'created',
            'product_id': instance.id,
            'title': instance.title,
        }
        group_send(group_name, event)
