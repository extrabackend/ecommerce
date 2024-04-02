from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/products/', consumers.ProductConsumer.as_asgi()),
]
