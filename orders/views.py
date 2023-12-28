from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


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
