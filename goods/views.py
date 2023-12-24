from django.shortcuts import render

from goods.models import Product


def catalog(request):
    goods = Product.objects.all()

    context = {
        "title": "House Style - Catalog",
        "goods": goods
    }
    return render(request=request, template_name="goods/catalog.html", context=context)


def product(request):
    return render(request=request, template_name="goods/product.html")
