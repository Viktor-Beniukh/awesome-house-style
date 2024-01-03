from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from goods.forms import CategoryForm
from goods.models import Product
from goods.utils import q_search


def catalog_view(request, category_slug: str = None):
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    goods = Product.objects.all()

    if category_slug and category_slug != "all-goods":
        goods = goods.filter(category__slug=category_slug)

    if query:
        goods = q_search(query)

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
        "title": f"House Style - {product.name}",
        "product": product
    }

    return render(
        request=request, template_name="goods/product.html", context=context
    )


def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
def category_create_view(request):
    if is_admin(request.user):
        if request.method == "POST":
            form = CategoryForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Category successfully created")
                return HttpResponseRedirect(reverse("main:index"))
        else:
            form = CategoryForm()

        context = {
            "title": "House Style - Create Category",
            "form": form
        }
        return render(
            request=request, template_name="goods/category_create.html", context=context
        )
    else:
        messages.warning(request, "You do not have permission to create categories.")
        return HttpResponseRedirect(reverse("main:index"))
