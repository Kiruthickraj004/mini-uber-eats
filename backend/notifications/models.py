from django.conf import settings
from django.db import models

from orders.models import Order


class NotificationType(models.TextChoices):
    ORDER_READY = "ORDER_READY", "Order Ready"


class NotificationChannel(models.TextChoices):
    EMAIL = "EMAIL", "Email"


class NotificationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"


class Notification(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="notifications",
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="notifications",
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
    )

    channel = models.CharField(
        max_length=20,
        choices=NotificationChannel.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
    )

    attempts = models.PositiveIntegerField(
        default=0,
    )

    last_error = models.TextField(
        blank=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "order",
                    "recipient",
                    "notification_type",
                    "channel",
                ],
                name="unique_order_notification",
            ),
        ]

    def __str__(self):
        return (
            f"Notification #{self.id} "
            f"- Order #{self.order_id}"
        )