from django.conf import settings
from django.db import models
from orders.models import Order

class DriverStatus(models.TextChoices):
    OFFLINE = "OFFLINE", "Offline"
    AVAILABLE = "AVAILABLE", "Available"
    BUSY = "BUSY", "Busy"


class DriverProfile(models.Model):
    Status = DriverStatus

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="driver_profile",
    )

    status = models.CharField(
        max_length=20,
        choices=DriverStatus.choices,
        default=DriverStatus.OFFLINE,
    )

    vehicle_type = models.CharField(
        max_length=50,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"DriverProfile #{self.id} - {self.user.username}"



class DeliveryStatus(models.TextChoices):
    ASSIGNED = "ASSIGNED", "Assigned"
    PICKED_UP = "PICKED_UP", "Picked Up"
    DELIVERED = "DELIVERED", "Delivered"


class Delivery(models.Model):
    Status = DeliveryStatus

    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="delivery",
    )

    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.PROTECT,
        related_name="deliveries",
    )

    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.ASSIGNED,
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    picked_up_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery #{self.id} - Order #{self.order_id}"