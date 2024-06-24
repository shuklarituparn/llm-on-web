from django.urls import path
from django.views.generic import TemplateView

app_name = "chat"
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/chat.html"), name="chat"),
    path(
        "llava/",
        TemplateView.as_view(template_name="pages/chat_llava.html"),
        name="llava",
    ),
    path(
        "llava/conversations/",
        TemplateView.as_view(template_name="pages/chat_llava.html"),
        name="llava_conversation",
    ),
]
