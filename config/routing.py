from django.urls import re_path

from config import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/guest/",
        consumers.ChatGuestConsumer.as_asgi(),
        name="chat_guest",
    ),
    re_path(r"ws/chat/user/", consumers.ChatUserConsumer.as_asgi(), name="chat_user"),
    re_path(
        r"ws/chat/llava/",
        consumers.ChatLlavaGConsumer.as_asgi(),
        name="llava_guest",
    ),
    re_path(
        r"ws/chat/llava/user/",
        consumers.ChatLlavaUConsumer.as_asgi(),
        name="llava_user",
    ),
]
