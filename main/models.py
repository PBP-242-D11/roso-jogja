import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CUSTOMER = "C"
    RESTAURANT_OWNER = "R"
    ADMIN = "A"
    ROLE_CHOICES = [
        (CUSTOMER, "Customer"),
        (RESTAURANT_OWNER, "Restaurant Owner"),
        (ADMIN, "Admin"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=CUSTOMER)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    class Meta:
        ordering = ["-date_joined"]
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.username
