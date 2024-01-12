from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "password")


class UserProfileForm(UserChangeForm):
    image_user = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "image_user",
            "first_name",
            "last_name",
            "username",
            "email",
        )
