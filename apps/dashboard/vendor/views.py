from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(
        request,
        "dashboard/vendor/pages/home.html",
    )


@login_required
def list_categories_view(request):
    return render(
        request,
        "dashboard/vendor/pages/categories.html",
    )
