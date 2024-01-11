from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Value, BooleanField
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from goods.forms import CategoryForm, ProductForm, ReviewForm
from goods.models import Product, FavoriteProduct
from goods.utils import q_search


def catalog_view(request, category_slug: str = None):
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    goods = Product.objects.all()

    favorite_products = []
    if request.user.is_authenticated:
        favorite_products = (
            FavoriteProduct.objects.filter(user=request.user)
            .values_list("product_id", flat=True)
        )

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
        "favorite_products": favorite_products,
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


@login_required
def product_create_view(request):
    if is_admin(request.user):
        if request.method == "POST":
            form = ProductForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Product successfully created")
                return HttpResponseRedirect(reverse("main:index"))
        else:
            form = ProductForm()

        context = {
            "title": "House Style - Create Product",
            "form": form
        }
        return render(
            request=request, template_name="goods/product_create.html", context=context
        )
    else:
        messages.warning(request, "You do not have permission to create products.")
        return HttpResponseRedirect(reverse("main:index"))


@login_required
def product_update_view(request, product_slug: str):
    product = get_object_or_404(Product, slug=product_slug)

    if is_admin(request.user):
        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product successfully updated")
                return HttpResponseRedirect(product.get_absolute_url())
        else:
            form = ProductForm(instance=product)

        context = {
            "title": "House Style - Update Product",
            "form": form
        }
        return render(
            request=request, template_name="goods/product_update.html", context=context
        )
    else:
        messages.warning(request, "You do not have permission to update products.")
        return HttpResponseRedirect(product.get_absolute_url())


@login_required
def product_delete_view(request, product_slug: str):
    product = get_object_or_404(Product, slug=product_slug)

    if is_admin(request.user):
        if request.method == "POST":
            product.delete()
            messages.success(request, "Product successfully removed")
            return HttpResponseRedirect(reverse("main:index"))

        context = {
            "title": "House Style - Remove Product",
            "product": product,
        }
        return render(
            request=request, template_name="goods/product_confirm_delete.html", context=context
        )
    else:
        messages.warning(request, "You do not have permission to remove products.")
        return HttpResponseRedirect(product.get_absolute_url())


@login_required
@require_POST
def create_review(request, product_id: int):
    data = request.POST.copy()
    data.update({"user": request.user.id})
    form = ReviewForm(data)
    product = Product.objects.get(id=product_id)

    if form.is_valid():
        review = form.save(commit=False)
        if request.POST.get("parent", None):
            review.parent_id = int(request.POST.get("parent"))
        review.user = request.user
        review.product = product
        review.save()

    return redirect(product.get_absolute_url())


@login_required
def favorite_products_view(request):
    user = request.user
    favorite_products = (
        FavoriteProduct.objects
        .filter(user=user)
        .select_related("product")
        .annotate(is_favorite=Value(True, output_field=BooleanField()))
    )

    context = {
        "title": "House Style - Favorite Products",
        "favorite_products": favorite_products,
    }

    return render(request, "goods/favorite_products.html", context)


@login_required
@csrf_exempt
def toggle_favorite_view(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id or not product_id.isdigit():
            return JsonResponse({"error": "Invalid product_id"}, status=400)

        user = request.user

        try:
            favorite_product = FavoriteProduct.objects.get(user=user, product_id=product_id)
            favorite_product.delete()
            is_favorite = False
        except FavoriteProduct.DoesNotExist:
            FavoriteProduct.objects.create(user=user, product_id=product_id)
            is_favorite = True

        favorites_count = user.favoriteproduct_set.count()

        return JsonResponse({"is_favorite": is_favorite, "favorites_count": favorites_count})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
