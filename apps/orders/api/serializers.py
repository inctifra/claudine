from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Used when a customer places an order.
    Public endpoint — no auth required.
    """

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "phone",
            "hostel_name",
            "room_number",
            "product",
            "quantity",
            "preferred_color",
            "notes",
        ]

    def validate_quantity(self, value):
        if value < 1:
            msg = "Quantity must be at least 1."
            raise serializers.ValidationError(msg)
        return value

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity", 1)

        if product and not product.is_active:
            raise serializers.ValidationError(
                {"product": "This product is no longer available."},
            )

        if product and product.stock_quantity < quantity:
            raise serializers.ValidationError(
                {"quantity":
                 f"Only {product.stock_quantity} items available in stock."},
            )

        return data


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Used for PUT/PATCH by the seller to update order details.
    """

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "phone",
            "hostel_name",
            "room_number",
            "product",
            "quantity",
            "preferred_color",
            "notes",
            "status",
            "admin_notes",
            "is_active",
        ]

    def validate(self, data):
        # Prevent changing product if order is already delivered
        instance = self.instance
        if instance and instance.status == "delivered" and "product" in data:
            raise serializers.ValidationError(
                {"product": "Cannot change product on a delivered order."},
            )
        return data


class OrderListSerializer(serializers.ModelSerializer):
    """
    Used for list and retrieve responses.
    Includes computed total_price and product details.
    """

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.IntegerField(source="product.price", read_only=True)
    product_image = serializers.SerializerMethodField()
    total_price = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "phone",
            "hostel_name",
            "room_number",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "quantity",
            "preferred_color",
            "total_price",
            "status",
            "status_display",
            "notes",
            "admin_notes",
            "is_active",
            "created_at",
            "updated_at",
        ]
    @extend_schema_field(field=serializers.URLField())
    def get_product_image(self, obj):
        img = obj.product.primary_image
        if img:
            return img.image.url
        return None


class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for status transition actions (confirm, deliver).
    Only accepts status field — used by custom actions.
    """

    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        allowed = ["pending", "confirmed", "delivered", "cancelled"]
        if value not in allowed:
            msg = f"Status must be one of: {', '.join(allowed)}."
            raise serializers.ValidationError(msg)
        return value
