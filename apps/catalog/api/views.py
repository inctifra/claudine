from bunifu_django_auth.apis.api_docs import delete_docs
from bunifu_django_auth.apis.api_docs import get_docs
from bunifu_django_auth.apis.api_docs import patch_docs
from bunifu_django_auth.apis.api_docs import post_docs
from bunifu_django_auth.apis.api_docs import put_docs
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.catalog.models import Category
from apps.catalog.models import Product

from .serializers import CategorySerializer
from .serializers import ProductCreateUpdateSerializer
from .serializers import ProductDetailSerializer
from .serializers import ProductListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoints for product categories.
    """

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "display_order", "created_at"]
    ordering = ["display_order", "name"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    # =========================================================
    # Standard CRUD
    # =========================================================

    @get_docs(
        summary="List categories",
        description="""
        Returns all product categories
        (Handwear, Neckwear, Ornaments, etc).""".strip(),
        tags=["Catalog - Categories"],
        operation_id="categories_list",
        responses=CategorySerializer,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @post_docs(
        summary="Create category",
        description="Creates a new product category.",
        tags=["Catalog - Categories"],
        operation_id="categories_create",
        request=CategorySerializer,
        responses=CategorySerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @get_docs(
        summary="Retrieve category",
        description="Returns a single category by slug.",
        tags=["Catalog - Categories"],
        operation_id="categories_retrieve",
        responses=CategorySerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @put_docs(
        summary="Update category",
        description="Fully updates a category.",
        tags=["Catalog - Categories"],
        operation_id="categories_update",
        request=CategorySerializer,
        responses=CategorySerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @patch_docs(
        summary="Partially update category",
        description="Partially updates a category.",
        tags=["Catalog - Categories"],
        operation_id="categories_partial_update",
        request=CategorySerializer,
        responses=CategorySerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @delete_docs(
        summary="Delete category",
        description="Soft-deletes a category (sets is_active=False).",
        tags=["Catalog - Categories"],
        operation_id="categories_delete",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoints for bead products.
    Public read access. Write operations require authentication.
    """

    queryset = (
        Product.objects.select_related("category").prefetch_related("images").all()
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "category__slug",
        "is_active",
        "stock_quantity",
    ]
    search_fields = [
        "name",
        "description",
        "colors",
    ]
    ordering_fields = [
        "price",
        "created_at",
        "stock_quantity",
        "name",
    ]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        action_serializer_map = {
            "list": ProductListSerializer,
            "create": ProductCreateUpdateSerializer,
            "retrieve": ProductDetailSerializer,
            "update": ProductCreateUpdateSerializer,
            "partial_update": ProductCreateUpdateSerializer,
        }
        return action_serializer_map.get(self.action, ProductDetailSerializer)

    def get_permissions(self):
        if self.action in ["list", "retrieve", "in_stock"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ["list", "retrieve", "in_stock"]:
            return qs.filter(is_active=True)
        return qs

    # =========================================================
    # Standard CRUD
    # =========================================================

    @get_docs(
        summary="List products",
        description="""
        Returns a paginated list of handmade bead products.
        Filter by category, search by color or name, sort by price.
        """.strip(),
        tags=["Catalog - Products"],
        operation_id="products_list",
        responses=ProductListSerializer,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @post_docs(
        summary="Create product",
        description="Adds a new bead product to the catalog.",
        tags=["Catalog - Products"],
        operation_id="products_create",
        request=ProductCreateUpdateSerializer,
        responses=ProductDetailSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @get_docs(
        summary="Retrieve product",
        description="""
        Returns full product details
        including all images and color options.""".strip(),
        tags=["Catalog - Products"],
        operation_id="products_retrieve",
        responses=ProductDetailSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @put_docs(
        summary="Update product",
        description="Fully updates a product. All fields required.",
        tags=["Catalog - Products"],
        operation_id="products_update",
        request=ProductCreateUpdateSerializer,
        responses=ProductDetailSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @patch_docs(
        summary="Partially update product",
        description="Updates only supplied fields (price, stock, colors, etc).",
        tags=["Catalog - Products"],
        operation_id="products_partial_update",
        request=ProductCreateUpdateSerializer,
        responses=ProductDetailSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @delete_docs(
        summary="Delete product",
        description="Soft-deletes a product.",
        tags=["Catalog - Products"],
        operation_id="products_delete",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # =========================================================
    # Custom Actions
    # =========================================================

    @get_docs(
        summary="In-stock products",
        description="Returns only products currently available (stock_quantity > 0).",
        tags=["Catalog - Products"],
        operation_id="products_in_stock",
        responses=ProductListSerializer,
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="in-stock",
        url_name="in-stock",
    )
    def in_stock(self, request):
        products = self.get_queryset().filter(stock_quantity__gt=0)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
