import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from products import routing

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(routing.websocket_urlpatterns),
    }
)
