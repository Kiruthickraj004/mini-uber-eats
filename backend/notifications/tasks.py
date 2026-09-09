try:
    from celery import shared_task  # type: ignore[reportMissingImports]
except ImportError:
    def shared_task(func):
        return func

from django.core.mail import send_mail
from orders.models import Order


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def notify_order_ready(order_id):
    order = (
        Order.objects
        .select_related("customer", "restaurant")
        .get(id=order_id)
    )

    send_mail(
        subject=f"Your order #{order.id} is ready",
        message=(
            f"Your order from {order.restaurant.name} "
            "is ready for delivery."
        ),
        from_email=None,
        recipient_list=[order.customer.email],
    )

    return {
        "order_id": order.id,
        "status": "NOTIFIED",
    }