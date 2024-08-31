from django.urls import path
from django.views.generic import TemplateView

from .views import llava_chat_view
from .views import user_chat_view

app_name = "chat"
urlpatterns = [
    path("", view=user_chat_view, name="chat"),
    path(
        "llava/",
        view=llava_chat_view,
        name="llava",
    ),
    path(
        "llava/conversations/",
        TemplateView.as_view(template_name="pages/chat_llava.html"),
        name="llava_conversation",
    ),
]

