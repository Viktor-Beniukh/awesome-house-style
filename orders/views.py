from django.shortcuts import render


def create_order_view(request):
    return render(request=request, template_name="orders/create_order.html")
