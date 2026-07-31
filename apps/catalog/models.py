from core.models import BaseModel
from django.db import models
from django.utils.text import slugify


class Category(BaseModel):
    """Handwear, Neckwear, Ornaments, etc."""

    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.SET_NULL,
        related_name="category_stores",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Categories"
        ordering = ["display_order", "name"]
        constraints = [
            models.UniqueConstraint(
                name="unique_store_category_and_name",
                fields=["store", "name"],
            ),
        ]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(help_text="Price in your local currency")
    stock_quantity = models.PositiveSmallIntegerField(default=1)
    colors = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated: Red, Blue, Green",
    )

    class Meta(BaseModel.Meta):
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (${self.price})"

    @property
    def primary_image(self):
        """Returns the first image or None"""
        return self.images.filter(is_primary=True).first() or self.images.first()

    @property
    def color_list(self):
        return [c.strip() for c in self.colors.split(",") if c.strip()]


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="products/%Y/%m/")
    is_primary = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        ordering = ["-is_primary", "-created_at"]

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary image per product
            ProductImage.objects.filter(product=self.product).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"
