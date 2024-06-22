from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from llm_on_web.users.forms import UserContactForm
from llm_on_web.users.forms import UserUpdateForm
from llm_on_web.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class UserConversationsView(LoginRequiredMixin, TemplateView):
    template_name = "users/conversations.html"


user_conversations_view = UserConversationsView.as_view()


class UserContactView(LoginRequiredMixin, FormView):
    template_name = "pages/contact.html"
    form_class = UserContactForm
    success_url = "/contact"

    def form_valid(self, form_class):
        email = form_class.cleaned_data["email"]
        subject = form_class.cleaned_data["subject"]
        message = form_class.cleaned_data["message"]

        if form_class.is_valid():
            EmailMessage(
                subject=f"Contact form submission about {subject}",
                body=message,
                from_email="rtprnshukla@gmail.com",
                to=[email],
            ).send(fail_silently=False)

            return super().form_valid(form_class)

        return redirect("contact")


user_contact_view = UserContactView.as_view()
