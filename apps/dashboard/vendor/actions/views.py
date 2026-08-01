# Copyright 2026 liont
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from apps.catalog.api.serializers import CategorySerializer
from apps.catalog.forms import CategoryModelForm
from apps.catalog.models import Category
from apps.stores.api.serializers import StoreSerializer
from apps.stores.forms import StoreModelForm


@login_required
@require_POST
def create_vendor_store_view(request):
    form = StoreModelForm(request.POST, owner=request.user)
    if form.is_valid():
        print(form.cleaned_data)
        instance = form.save()
        serializer = StoreSerializer(instance=instance, context={"request": request})
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(form.errors.as_json(), status=400)


@login_required
@require_POST
def create_category_view(request):
    form = CategoryModelForm(request.POST, store=request.user.store)
    if form.is_valid():
        form.save()
        return render(
            request,
            "dashboard/vendor/pages/components/category_tb_row.html",
            {
                "categories": Category.objects.filter(store=request.user.store),
            },
        )
    return JsonResponse(form.errors.as_json(), status=400)
