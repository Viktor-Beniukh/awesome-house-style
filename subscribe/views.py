import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from subscribe.forms import SubscribeForm
from subscribe.models import Subscriber

logger = logging.getLogger(__name__)


class SubscribeView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subscriber
    form_class = SubscribeForm
    template_name = "subscribe/tags/subscribe_form.html"
    success_url = reverse_lazy("main:index")

    success_message = "You subscribed successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user

        if Subscriber.objects.filter(user=user).exists():
            logger.info("You are already subscribed.")
            messages.info(self.request, "You are already subscribed.")
            return HttpResponseRedirect(self.success_url)

        form.save(commit=False)
        form.instance.user = user
        form.save()

        return super().form_valid(form)


class UnsubscribeView(LoginRequiredMixin, TemplateView):
    template_name = "subscribe/unsubscribe_confirm.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        Subscriber.objects.filter(user=user).delete()

        logger.info("You have been unsubscribed.")
        messages.success(request, "You have been unsubscribed.")
        return redirect(reverse_lazy("main:index"))
