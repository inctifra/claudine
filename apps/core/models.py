import uuid

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing common fields for all models.
    Inherit from this for consistent timestamps, UUIDs, and soft-delete.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text="Unique identifier for the record",
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, help_text="When this record was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When this record was last modified",
    )

    # Soft delete (better than hard delete for order history)
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Soft-delete flag. Set False instead of deleting.",
    )

    # Audit trail (optional but useful if you add admin users later)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        help_text="User who created this record",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        help_text="User who last updated this record",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    def soft_delete(self):
        """Soft delete this instance instead of removing from database."""
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def restore(self):
        """Restore a soft-deleted instance."""
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])
