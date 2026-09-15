try:
    from celery import shared_task  # type: ignore[reportMissingImports]
except ImportError:
    def shared_task(func):
        return func

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from orders.models import Order
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Notification, NotificationStatus


@shared_task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def notify_order_ready(self, notification_id):
    with transaction.atomic():
        notification = (
            Notification.objects
            .select_for_update()
            .select_related(
                "order",
                "order__restaurant",
                "recipient",
            )
            .get(id=notification_id)
        )

        if notification.status == NotificationStatus.SENT:
            return {
                "notification_id": notification.id,
                "status": "ALREADY_SENT",
            }

        notification.status = NotificationStatus.PROCESSING
        notification.attempts += 1
        notification.save(
            update_fields=[
                "status",
                "attempts",
                "updated_at",
            ]
        )

    send_mail(
        subject=f"Your order #{notification.order.id} is ready",
        message=(
            f"Your order from "
            f"{notification.order.restaurant.name} "
            "is ready for delivery."
        ),
        from_email=None,
        recipient_list=[notification.recipient.email],
    )

    with transaction.atomic():
        notification = (
            Notification.objects
            .select_for_update()
            .get(id=notification_id)
        )

        notification.status = NotificationStatus.SENT
        notification.sent_at = timezone.now()
        notification.last_error = ""
        notification.save(
            update_fields=[
                "status",
                "sent_at",
                "last_error",
                "updated_at",
            ]
        )

    return {
        "notification_id": notification.id,
        "status": "SENT",
    }

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def notify_available_drivers(self, order_id):
    print(
        f"Notification: Drivers notified for order #{order_id}."
    )

    return {
        "order_id": order_id,
        "status": "DRIVERS_NOTIFIED",
    }


@shared_task
def check_stuck_notifications():
    threshold = timezone.now() - timedelta(minutes=10)

    notifications = Notification.objects.filter(
        status=NotificationStatus.PROCESSING,
        updated_at__lt=threshold,
    )

    count = notifications.count()

    print(
        f"Found {count} stuck notifications."
    )

    return {
        "stuck_notifications": count,
    }

@shared_task
def record_notification_completion(result):
    print(
        f"Notification {result['notification_id']} completed successfully."
    )

    return {
        **result,
        "completion_recorded": True,
    }

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def notify_driver(self, driver_id, order_id):
    try:
        print(
            f"Notifying driver {driver_id} about order {order_id}"
        )

        return {
            "driver_id": driver_id,
            "order_id": order_id,
            "notified": True,
            "error": None,
        }

    except Exception as exc:
        return {
            "driver_id": driver_id,
            "order_id": order_id,
            "notified": False,
            "error": str(exc),
        }

@shared_task
def process_driver_notification_results(results):
    successful = sum(
        1
        for result in results
        if result.get("notified") is True
    )

    failed = len(results) - successful

    print(
        f"Driver notification batch completed: "
        f"{successful} successful, {failed} failed"
    )

    return {
        "total": len(results),
        "successful": successful,
        "failed": failed,
    }