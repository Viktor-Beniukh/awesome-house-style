from django.shortcuts import render

from goods.models import Product


def catalog(request):
    goods = Product.objects.all()

    context = {
        "title": "House Style - Catalog",
        "goods": goods
    }

    return render(
        request=request, template_name="goods/catalog.html", context=context
    )


def product_view(request, product_slug: str):
    product = Product.objects.get(slug=product_slug)

    context = {
        "product": product
    }

    return render(
        request=request, template_name="goods/product.html", context=context
    )
