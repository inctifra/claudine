from core.models import BaseModel
from django.core.validators import RegexValidator
from django.db import models


class Order(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(max_length=150)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="""
        Phone number must be entered in format:
        '+999999999'. Up to 15 digits allowed.""",
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)

    # Location details for hostel delivery
    hostel_name = models.CharField(
        max_length=200, help_text="e.g., Queen's Hostel, Block A",
    )
    room_number = models.CharField(
        max_length=50, blank=True, help_text="e.g., Room 204",
    )

    # Order details
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.PROTECT, related_name="orders",
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    preferred_color = models.CharField(max_length=100, blank=True)
    notes = models.TextField(
        blank=True, help_text="Any special requests or delivery instructions",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Admin tracking
    admin_notes = models.TextField(blank=True, help_text="Internal notes")

    class Meta(BaseModel.Meta):
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{str(self.id)[:8]} - {self.customer_name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
