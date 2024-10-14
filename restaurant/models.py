import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Restaurant(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    address = models.TextField(blank=True)
    price_range = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(
        "main.User",
        on_delete=models.CASCADE,
        related_name="restaurants",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="foods"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Menambahkan Meta class untuk mengatur pengurutan data
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"

    def __str__(self):
        return f"{self.name} at {self.restaurant.name}"

    # Override metode save() untuk membuat slug otomatis
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.restaurant.name}-{self.name}")
        super().save(*args, **kwargs)
