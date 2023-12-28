from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("user:logout"):
                    return HttpResponseRedirect(request.POST.get("next"))

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
    return render(request, "users/users_cart.html")


@login_required
def logout_view(request):
    messages.success(request, f"{request.user.username}, You left your account")
    auth.logout(request)
    return redirect(reverse("main:index"))
