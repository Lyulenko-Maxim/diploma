from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.scope['user']

    async def connect(self):
        if self.user == AnonymousUser():
            await self.close()

        await self.accept()
        self.connections_increment()

    async def disconnect(self, close_code):
        if self.user == AnonymousUser():
            await super().disconnect(close_code)

        self.connections_decrement()
        await super().disconnect(close_code)

    @database_sync_to_async
    def connections_increment(self):
        self.user.connections += 1
        self.user.save(update_fields=['connections'])


    @database_sync_to_async
    def connections_decrement(self, user):
        self.user.connections -= 1
        self.user.save(update_fields=['connections'])

