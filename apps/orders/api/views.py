from bunifu_django_auth.apis.api_docs import delete_docs
from bunifu_django_auth.apis.api_docs import get_docs
from bunifu_django_auth.apis.api_docs import patch_docs
from bunifu_django_auth.apis.api_docs import post_docs
from bunifu_django_auth.apis.api_docs import put_docs
from django.db import models
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order

from .serializers import OrderCreateSerializer
from .serializers import OrderListSerializer
from .serializers import OrderStatusSerializer
from .serializers import OrderUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoints for customer orders.
    Anyone can create an order. Only authenticated users can list/manage them.
    """

    queryset = (
        Order.objects.select_related("product", "product__category")
        .prefetch_related("product__images")
        .all()
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "status",
        "is_active",
        "hostel_name",
        "product",
    ]
    search_fields = [
        "customer_name",
        "phone",
        "hostel_name",
        "room_number",
    ]
    ordering_fields = [
        "created_at",
        "status",
        "hostel_name",
    ]
    ordering = ["-created_at"]
    lookup_field = "pk"

    def get_serializer_class(self):
        action_serializer_map = {
            "list": OrderListSerializer,
            "create": OrderCreateSerializer,
            "retrieve": OrderListSerializer,
            "update": OrderUpdateSerializer,
            "partial_update": OrderUpdateSerializer,
            "mark_confirmed": OrderStatusSerializer,
            "mark_delivered": OrderStatusSerializer,
        }
        return action_serializer_map.get(self.action, OrderListSerializer)

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    # =========================================================
    # Standard CRUD
    # =========================================================

    @get_docs(
        summary="List orders",
        description="Returns a paginated list of all customer orders.",
        tags=["Orders"],
        operation_id="orders_list",
        responses=OrderListSerializer,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @post_docs(
        summary="Create order",
        description="""
        Places a new order. Requires customer name, phone, hostel, and product.
        No authentication required — students can order directly.
        """.strip(),
        tags=["Orders"],
        operation_id="orders_create",
        request=OrderCreateSerializer,
        responses=OrderListSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @get_docs(
        summary="Retrieve order",
        description="Returns detailed information for a specific order.",
        tags=["Orders"],
        operation_id="orders_retrieve",
        responses=OrderListSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @put_docs(
        summary="Update order",
        description="Fully updates an order.",
        tags=["Orders"],
        operation_id="orders_update",
        request=OrderUpdateSerializer,
        responses=OrderListSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @patch_docs(
        summary="Partially update order",
        description="Partially updates an order.",
        tags=["Orders"],
        operation_id="orders_partial_update",
        request=OrderUpdateSerializer,
        responses=OrderListSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @delete_docs(
        summary="Delete order",
        description="Soft-deletes an order.",
        tags=["Orders"],
        operation_id="orders_delete",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # =========================================================
    # Custom Actions
    # =========================================================

    @get_docs(
        summary="Pending orders",
        description="Returns orders awaiting confirmation or delivery.",
        tags=["Orders - Management"],
        operation_id="orders_pending",
        responses=OrderListSerializer,
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="pending",
        url_name="pending",
    )
    def pending(self, request):
        orders = self.get_queryset().filter(
            status__in=["pending", "confirmed"],
            is_active=True,
        )
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    @get_docs(
        summary="Today's orders",
        description="Returns all orders placed today.",
        tags=["Orders - Management"],
        operation_id="orders_today",
        responses=OrderListSerializer,
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="today",
        url_name="today",
    )
    def today(self, request):
        today = timezone.now().date()
        orders = self.get_queryset().filter(created_at__date=today)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    @get_docs(
        summary="Orders by hostel",
        description="""
        Returns orders grouped by hostel name.
        Perfect for planning delivery routes when walking between hostels.
        """.strip(),
        tags=["Orders - Management"],
        operation_id="orders_by_hostel",
        responses=OrderListSerializer,
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="by-hostel",
        url_name="by-hostel",
    )
    def by_hostel(self, request):
        orders = (
            self.get_queryset()
            .filter(status__in=["pending", "confirmed"], is_active=True)
            .order_by("hostel_name", "room_number")
        )
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    @post_docs(
        summary="Confirm order",
        description="Marks an order as confirmed (ready for delivery).",
        tags=["Orders - Management"],
        operation_id="orders_mark_confirmed",
        request=OrderStatusSerializer,
        responses=OrderListSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="confirm",
        url_name="confirm",
    )
    def mark_confirmed(self, request, pk=None):
        order = self.get_object()
        order.status = "confirmed"
        order.save(update_fields=["status", "updated_at"])
        serializer = OrderListSerializer(order)
        return Response(serializer.data)

    @post_docs(
        summary="Deliver order",
        description="Marks an order as delivered.",
        tags=["Orders - Management"],
        operation_id="orders_mark_delivered",
        request=OrderStatusSerializer,
        responses=OrderListSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="deliver",
        url_name="deliver",
    )
    def mark_delivered(self, request, pk=None):
        order = self.get_object()
        order.status = "delivered"
        order.save(update_fields=["status", "updated_at"])
        serializer = OrderListSerializer(order)
        return Response(serializer.data)

    @get_docs(
        summary="Order statistics",
        description="Returns daily stats: total orders, revenue, pending count.",
        tags=["Orders - Analytics"],
        operation_id="orders_stats",
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="stats",
        url_name="stats",
    )
    def stats(self, request):
        today = timezone.now().date()
        orders_today = Order.objects.filter(created_at__date=today, is_active=True)

        data = {
            "total_orders_today": orders_today.count(),
            "pending_orders": orders_today.filter(status="pending").count(),
            "confirmed_orders": orders_today.filter(status="confirmed").count(),
            "delivered_today": orders_today.filter(status="delivered").count(),
            "total_revenue_today": orders_today.filter(
                status="delivered",
                product__price__isnull=False,
            ).aggregate(
                total=models.Sum(
                    models.F("product__price") * models.F("quantity"),
                ),
            )["total"]
            or 0,
            "top_hostel_today": (
                orders_today.values("hostel_name")
                .annotate(count=models.Count("id"))
                .order_by("-count")
                .first()
            ),
        }

        return Response(data)
