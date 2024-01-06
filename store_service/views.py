from django.shortcuts import render


def custom_404(request, exception=None):
    context = {
        "title": "House Style - Page Not Found"
    }
    return render(request, template_name="404.html", status=404, context=context)


def custom_500(request):
    context = {
        "title": "House Style - Server Error"
    }
    return render(request, template_name="500.html", status=500, context=context)
