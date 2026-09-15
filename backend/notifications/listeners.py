from orders.models import Order
from .workflows import notify_available_drivers_workflow
from notifications.models import (
    Notification,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
)
from orders.events import OrderReady

from .tasks import (
    notify_order_ready,
    notify_available_drivers,
)


def handle_order_ready(event: OrderReady):
    order = (
        Order.objects
        .select_related("customer")
        .get(id=event.order_id)
    )

    notification, created = Notification.objects.get_or_create(
        order=order,
        recipient=order.customer,
        notification_type=NotificationType.ORDER_READY,
        channel=NotificationChannel.EMAIL,
        defaults={
            "status": NotificationStatus.PENDING,
        },
    )

    if created:
        notify_order_ready.delay(notification.id)

    notify_available_drivers_workflow(order.id)