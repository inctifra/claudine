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

from django.db import models
from django.db.models import Count
from django.db.models import Q


class CategoryManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("store")
            .order_by("display_order", "name")
        )

    def for_store(self, store):
        """Categories belonging to a specific store, with product counts."""
        return (
            self.filter(store=store)
            .annotate(product_count=Count("products", distinct=True))
            .order_by("display_order", "name")
        )

    def active_for_store(self, store):
        """Only active categories with at least one product."""
        return self.for_store(store).filter(products__isnull=False).distinct()

    def with_product_stats(self):
        """Annotate with total products and low stock count."""

        return self.annotate(
            product_count=Count("products", distinct=True),
            low_stock_count=Count(
                "products",
                filter=Q(products__stock_quantity__lte=5),
                distinct=True,
            ),
        )


class ProductManager(models.Manager):
    def for_store(self, store):
        """Products belonging to categories of a specific store."""
        return self.filter(category__store=store)

    def in_stock(self):
        """Products with available stock."""
        return self.filter(stock_quantity__gt=0)

    def low_stock(self, threshold=5):
        """Products running low on stock."""
        return self.filter(stock_quantity__gt=0, stock_quantity__lte=threshold)

    def out_of_stock(self):
        """Products with zero stock."""
        return self.filter(stock_quantity=0)

    def with_category(self):
        """Select related category to avoid N+1."""
        return self.select_related("category")

    def full_detail(self):
        """Optimized for detail views — everything joined/prefetched."""
        return self.select_related("category").prefetch_related("images")

    def dashboard_summary(self, store):
        """All counts needed for the vendor dashboard."""
        qs = self.for_store(store)
        return {
            "total": qs.count(),
            "in_stock": qs.in_stock().count(),
            "low_stock": qs.low_stock().count(),
            "out_of_stock": qs.out_of_stock().count(),
        }


class ProductImageManager(models.Manager):
    def for_product(self, product):
        return self.filter(product=product).order_by("-is_primary", "-created_at")

    def set_primary(self, image):
        """Make this image primary and demote all others for the same product."""
        self.filter(product=image.product).exclude(pk=image.pk).update(is_primary=False)
        image.is_primary = True
        image.save(update_fields=["is_primary"])
