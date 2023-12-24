from django.shortcuts import render, get_object_or_404

from goods.models import Product


def catalog(request, category_slug: str):
    if category_slug == "all-goods":
        goods = Product.objects.all()
    else:
        goods = get_object_or_404(Product.objects.filter(category__slug=category_slug))

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
