import logging

from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator

from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm

logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=email, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("user:logout"):
                    return HttpResponseRedirect(request.POST.get("next"))

                logger.info(f"Welcome {user.username} to our site")
                messages.success(request, f"Welcome {user.username} to our site")
                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "House Style - Authorization",
        "form": form
    }

    return render(request=request, template_name="users/login.html", context=context)


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            logger.info(f"{user.username}, You have successfully registered and logged in")
            messages.success(request, f"{user.username}, You have successfully registered and logged in")
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegisterForm()

    context = {
        "title": "House Style - Registration",
        "form": form
    }
    return render(request=request, template_name="users/register.html", context=context)


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()

            logger.info("Profile successfully updated")
            messages.success(request, "Profile successfully updated")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = UserProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "order_items",
            queryset=OrderItem.objects.select_related("product"),
        )
    ).order_by("-id")

    context = {
        "title": "House Style - Personal Account",
        "form": form,
        "orders": orders,
    }
    return render(request=request, template_name="users/profile.html", context=context)


def users_cart_view(request):
    context = {
        "title": "House Style - User Cart",
    }
    return render(request=request, template_name="users/users_cart.html", context=context)


@login_required
def logout_view(request):
    logger.info(f"{request.user.username}, You left your account")
    messages.success(request, f"{request.user.username}, You left your account")
    auth.logout(request)
    return redirect(reverse("main:index"))


@login_required
def change_password_view(request, pk):
    user = request.user

    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            logger.info("Password changed successfully.")
            messages.success(request, "Password changed successfully.")

            return redirect(reverse("user:password-success"))
    else:
        form = PasswordChangeForm(user)

    context = {
        "title": "House Style - Change Password",
        "form": form,
        "user": user
    }

    return render(request=request, template_name="users/password_change_form.html", context=context)


@login_required
def password_success_view(request):

    context = {
        "title": "House Style - Changed Password",
    }
    return render(
        request=request, template_name="users/password_change_done.html", context=context
    )


def reset_password_view(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save(
                request=request,
                email_template_name="users/password_reset_email.html",
            )

            logger.info("Message sent successfully.")
            messages.success(request, "Message sent successfully.")
            return redirect(reverse("user:password_reset_done"))

    context = {
        "title": "House Style - Reset Password",
        "form": form,
    }

    return render(
        request=request, template_name="users/password_reset_form.html", context=context
    )


def reset_password_done_view(request):
    context = {
        "title": "House Style - Reset Password Done"
    }

    return render(
        request=request, template_name="users/password_reset_done.html", context=context
    )


def reset_password_confirm_view(request, uidb64, token):
    user_id = urlsafe_base64_decode(uidb64).decode("utf-8")
    user = get_user_model().objects.get(pk=user_id)

    if default_token_generator.check_token(user, token):
        validlink = True

        if request.method == "POST":
            form = SetPasswordForm(data=request.POST, user=user)
            if form.is_valid():
                form.save()

                logger.info("Password reset successfully.")
                messages.success(request, "Password reset successfully.")
                return redirect(reverse("user:password_reset_complete"))
        else:
            form = SetPasswordForm(user=user)
    else:
        validlink = False
        form = None

    context = {
        "title": "House Style - Password Confirm",
        "validlink": validlink,
        "form": form,
        "uid": uidb64,
        "token": token,
    }

    return render(
        request=request, template_name="users/password_reset_confirm.html", context=context
    )


def reset_password_complete_view(request):
    context = {
        "title": "House Style - Password Complete"
    }

    return render(
        request=request, template_name="users/password_reset_complete.html", context=context
    )
