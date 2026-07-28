from django.contrib import admin

from .models import Category
from .models import Product
from .models import ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "display_order", "is_active", "created_at"]
    list_editable = ["display_order"]
    list_filter = ["is_active", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name", "category", "price", "stock_quantity", "is_active", "created_at"]
    list_filter = ["category", "is_active", "created_at"]
    list_editable = ["price", "stock_quantity"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    date_hierarchy = "created_at"
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "is_primary", "created_at"]
    list_filter = ["is_primary", "created_at"]
    readonly_fields = ["id", "created_at", "updated_at"]
