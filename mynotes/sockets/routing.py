from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('testing/', consumers.MyConsumer.as_asgi()),
]
