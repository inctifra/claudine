from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render

from apps.catalog.forms import CategoryModelForm, ProductForm, ProductImageFormSet
from apps.catalog.models import Category, Product


@login_required
def home(request):
    return render(
        request,
        "dashboard/vendor/pages/home.html",
    )


@login_required
def list_categories_view(request):
    context = {
        "categories": Category.objects.filter(
            store=request.user.store,
        ).prefetch_related("store"),
        "category_form": CategoryModelForm(store=request.user.store),
    }
    print("Categories:", context["categories"])  # Debugging line
    return render(
        request,
        "dashboard/vendor/pages/categories.html",
        context=context,
    )


@login_required
def list_products_view(request):
    products = Product.objects.filter(
        Q(category__store=request.user.store),
        Q(category__isnull=False),
        Q(category__is_active=True),
    ).select_related("category")

    return render(
        request,
        "dashboard/vendor/pages/products.html",
        {
            "products": products,
            "categories": Category.objects.filter(store=request.user.store),
        },
    )


@login_required
def create_product_view(request):
    store = request.user.store

    if request.method == "POST":
        form = ProductForm(request.POST, store=store)
        formset = ProductImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                product = form.save()
                images = formset.save(commit=False)
                for image in images:
                    image.product = product
                    image.save()
                # Handle deleted images
                formset.save_m2m()

            messages.success(request, "Product created successfully.")
            return redirect("dashboard:vendor:products_list_view")
    else:
        form = ProductForm(store=store)
        formset = ProductImageFormSet()

    return render(
        request,
        "dashboard/vendor/pages/create_product.html",
        {
            "form": form,
            "formset": formset,
        },
    )
