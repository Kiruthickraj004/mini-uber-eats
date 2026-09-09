from notifications.listeners import handle_order_ready
from orders.events import OrderReady


def dispatch(event):
    if isinstance(event, OrderReady):
        handle_order_ready(event)