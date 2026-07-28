from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.catalog.models import Category
from apps.catalog.models import Product
from apps.catalog.models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "created_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "is_active", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_name",
            "price",
            "is_active",
            "stock_quantity",
            "primary_image",
            "colors",
            "created_at",
        ]
    @extend_schema_field(field=serializers.JSONField())
    def get_primary_image(self, obj):
        img = obj.primary_image
        if img:
            return {"url": img.image.url, "id": str(img.id)}
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    color_list = serializers.ListField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "description",
            "price",
            "is_active",
            "stock_quantity",
            "colors",
            "color_list",
            "images",
            "created_at",
            "updated_at",
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used for POST, PUT, PATCH on products.
    Handles slug generation and category linking.
    """

    category_slug = serializers.SlugRelatedField(
        queryset=Category.objects.filter(is_active=True),
        slug_field="slug",
        source="category",
        required=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category_slug",
            "description",
            "price",
            "stock_quantity",
            "colors",
            "is_active",
        ]

    def validate_price(self, value):
        if value <= 0:
            msg = "Price must be greater than zero."
            raise serializers.ValidationError(msg)
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            msg = "Stock quantity cannot be negative."
            raise serializers.ValidationError(msg)
        return value
