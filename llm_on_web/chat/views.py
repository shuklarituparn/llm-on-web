from datetime import datetime

import pytz
from django.shortcuts import render
from django.views.generic import TemplateView

from llm_on_web.users.models import User

from .models import Chatid


class ChatMixin:
    def handle_authenticated_user(self, request):
        current_user = User.objects.get(pk=request.user.pk)
        chat_title = str(datetime.now(pytz.utc))
        newchat = Chatid.objects.create(chat_title=chat_title)
        newchat.userid = current_user
        newchat.save()
        current_chat_id = newchat.chatid
        current_user.currentchatid = current_chat_id
        current_user.save()


class ChatView(ChatMixin, TemplateView):
    template_name = "pages/chat.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.handle_authenticated_user(request)
        return render(request, self.template_name)


user_chat_view = ChatView.as_view()


class LlavaChatView(ChatMixin, TemplateView):
    template_name = "pages/chat_llava.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.handle_authenticated_user(request)
        return render(request, self.template_name)


llava_chat_view = LlavaChatView.as_view()
