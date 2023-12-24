from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Product
from goods.utils import q_search


def catalog_view(request, category_slug: str = None):
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    if category_slug == "all-goods":
        goods = Product.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

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
