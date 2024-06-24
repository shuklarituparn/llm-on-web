from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView


class ConversationView(FormMixin, ListView):
    def post(self):
        pass
