from django.conf import settings
from django.db import models


class Restaurant(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"
        SUSPENDED = "SUSPENDED", "Suspended"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(
        blank=True,
    )

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CLOSED,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name