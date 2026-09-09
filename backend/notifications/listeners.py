from orders.events import OrderReady

from .tasks import notify_order_ready


def handle_order_ready(event: OrderReady):
    notify_order_ready.delay(event.order_id)