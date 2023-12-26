from django.shortcuts import render, redirect

from carts.models import Cart
from goods.models import Product


def cart_add_view(request, product_slug: str):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    return redirect(request.META["HTTP_REFERER"])


def cart_change_view(request, product_slug: str):
    pass


def cart_remove_view(request, product_slug: str):
    pass
