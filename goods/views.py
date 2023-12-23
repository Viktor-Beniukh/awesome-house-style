from django.shortcuts import render


def catalog(request):
    context = {
        "title": "House Style - Catalog",
    }
    return render(request=request, template_name="goods/catalog.html", context=context)


def product(request):
    return render(request=request, template_name="goods/product.html")
