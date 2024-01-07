from django import forms

from subscribe.models import Subscriber


class SubscribeForm(forms.ModelForm):
    """Email Subscription Form"""
    is_subscribed = forms.BooleanField(required=True)

    class Meta:
        model = Subscriber
        fields = ("is_subscribed", "email")
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "class": "editContent",
                    "placeholder": "Your Email..."
                }
            )
        }
        labels = {
            "email": ""
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = user.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
