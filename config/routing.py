from django.urls import path

from config import consumers

websocket_urlpatterns = [
    path("ws/chat/", consumers.ChatGuestConsumer.as_asgi(), name="chat_guest"),
    path("ws/chat/user/", consumers.ChatUserConsumer.as_asgi(), name="chat_user"),
    path("ws/chat/llava", consumers.ChatLlavaGConsumer().as_asgi(), name="llava_guest"),
    path(
        "ws/chat/llava/user",
        consumers.ChatLlavaUConsumer.as_asgi(),
        name="llava_user",
    ),
]
