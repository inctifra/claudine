from django.db import models
from django.utils.text import slugify

from apps.core.models import BaseModel


class Store(BaseModel):
    owner = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="store"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
