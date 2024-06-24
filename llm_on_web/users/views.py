from allauth.account.models import EmailAddress
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
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        new_email = form.cleaned_data.get("email")
        email_address = EmailAddress.objects.filter(user=self.object).first()
        if email_address:
            email_address.email = new_email
            email_address.save()
        else:
            EmailAddress.objects.create(
                user=self.object,
                email=new_email,
                verified=True,
                primary=True,
            )
        return response


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class UserConversationsView(LoginRequiredMixin, TemplateView):
    template_name = "users/conversations.html"

    #  TODO: To get the list of conversations and render the conversations
    #  TODO: To change it from Templateview to the list


user_conversations_view = UserConversationsView.as_view()


class UserContactView(LoginRequiredMixin, FormView):
    template_name = "pages/contact.html"
    form_class = UserContactForm
    success_url = "/contact"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        if form.is_valid():
            EmailMessage(
                subject=f"Contact form submission about {subject}",
                body=message,
                from_email="rtprnshukla@gmail.com",
                to=[email],
            ).send(fail_silently=False)

            return super().form_valid(form)

        return redirect("contact")


user_contact_view = UserContactView.as_view()
