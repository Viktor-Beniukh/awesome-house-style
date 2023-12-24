from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Product


def catalog(request, category_slug: str = None):
    if category_slug == "all-goods":
        goods = Product.objects.all()
    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    page = request.GET.get("page", 1)
    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        "title": "House Style - Catalog",
        "goods": current_page,
        "slug_url": category_slug
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
