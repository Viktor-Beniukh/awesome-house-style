from django import template
from subscribe.forms import SubscribeForm

register = template.Library()


@register.inclusion_tag("subscribe/tags/subscribe_form.html")
def get_subscribe_form(user):
    return {"subscribe_form": SubscribeForm(user)}
