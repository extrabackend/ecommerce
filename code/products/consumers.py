from channels.db import database_sync_to_async
from channels.generic import websocket


class ProductConsumer(websocket.AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = 'new-products'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        event = {
            'type': 'new.product.created',
            **content,
        }
        await self.channel_layer.group_send(self.group_name, event)

    async def new_product_created(self, event):
        await self.send_json(event)
