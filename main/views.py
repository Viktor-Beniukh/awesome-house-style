from django.shortcuts import render


def index(request):
    context = {
        "title": "House Style - Home Page",
        "content": "Furniture store HouseStyle",
    }
    return render(request=request, template_name="index.html", context=context)
