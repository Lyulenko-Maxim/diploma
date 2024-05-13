from django.urls import path

from src.notifications.consumers import OnlineStatusConsumer

websocket_urlpatterns = [
    path('ws/', OnlineStatusConsumer.as_asgi()),
]
