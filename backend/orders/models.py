from django.conf import settings
from django.db import models

from menus.models import MenuItem
from restaurants.models import Restaurant


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready"
        DRIVER_ASSIGNED = "DRIVER_ASSIGNED", "Driver Assigned"
        PICKED_UP = "PICKED_UP", "Picked Up"
        DELIVERED = "DELIVERED", "Delivered"
        REJECTED = "REJECTED", "Rejected"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    name_snapshot = models.CharField(
        max_length=150,
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return (
            f"{self.name_snapshot} "
            f"x {self.quantity}"
        )