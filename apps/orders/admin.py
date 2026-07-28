from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id", "customer_name", "phone", "hostel_name",
        "product", "quantity", "status", "is_active", "created_at",
    ]
    list_filter = ["status", "is_active", "created_at", "hostel_name"]
    search_fields = ["customer_name", "phone", "hostel_name"]
    readonly_fields = ["id", "created_at", "updated_at", "total_price"]
    list_editable = ["status"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Customer", {
            "fields": ("customer_name", "phone", "hostel_name", "room_number"),
        }),
        ("Order", {
            "fields": ("product", "quantity", "preferred_color", "notes"),
        }),
        ("Status", {
            "fields": ("status", "is_active", "admin_notes", "total_price"),
        }),
        ("Audit", {
            "fields": ("id", "created_at", "updated_at", "created_by", "updated_by"),
            "classes": ("collapse",),
        }),
    )
