import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


BASE_URL = settings.BASE_URL
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_order_view(request):
    if request.method == "POST":
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            email=form.cleaned_data["email"],
                            phone_number=form.cleaned_data["phone_number"],
                            requires_delivery=form.cleaned_data["requires_delivery"],
                            shipping_address=form.cleaned_data["shipping_address"],
                            city=form.cleaned_data["city"],
                            country=form.cleaned_data["country"],
                            zipcode=form.cleaned_data["zipcode"],
                            payment_on_get=form.cleaned_data["payment_on_get"],
                        )

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Insufficient quantity of goods {name} in stock. Available - {product.quantity}"
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        cart_items.delete()

                        messages.success(request, "Order is made!")
                        return redirect("users:profile")
            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect("cart:order")
    else:
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        "title": "House Style - Making of Order",
        "form": form,
        "orders": True,
    }
    return render(request=request, template_name="orders/create_order.html", context=context)


@require_http_methods(["GET"])
def create_checkout_session(request, *args, **kwargs):
    order_id = kwargs["pk"]
    order = Order.objects.get(id=order_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(order.order_items.total_price() * 100),
                    "product_data": {
                        "name": f"Order №{order.id}",
                        "description": "Payment of the order",
                    },
                },
                "quantity": 1,
            },
        ],
        metadata={
            "order_id": order.id
        },
        mode="payment",
        success_url=BASE_URL + "/orders/success/",
        cancel_url=BASE_URL + "/orders/cancel/",
    )

    order.session_id = checkout_session.id
    order.session_url = checkout_session.url
    order.save()

    return redirect(order.session_url)


def success_view(request):
    orders = Order.objects.all()
    for order in orders:
        if order.session_id:
            order.status_payment = Order.PAID
            order.is_paid = True
            order.status_order = Order.SHIPPED
            order.paid_amount = order.order_items.total_price()

            order.save()

    context = {
        "title": "House Style - Payment Success"
    }

    return render(request, "orders/success.html", context=context)


def cancel_view(request):
    orders = Order.objects.all()

    for order in orders:
        if order.session_id and order.is_paid is False:
            order.status_payment = Order.CANCELLED

            order.save()

    context = {
        "title": "House Style - Payment Cancelled"
    }

    return render(request, "orders/cancel.html", context=context)
