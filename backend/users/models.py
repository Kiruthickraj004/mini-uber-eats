from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        RESTAURANT_OWNER = "RESTAURANT_OWNER", "Restaurant Owner"
        DRIVER = "DRIVER", "Driver"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
