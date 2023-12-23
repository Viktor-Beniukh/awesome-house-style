from django.shortcuts import render


def catalog(request):
    return render(request=request, template_name="catalog.html")


def product(request):
    return render(request=request, template_name="product.html")
