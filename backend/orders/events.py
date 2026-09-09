from dataclasses import dataclass


@dataclass(frozen=True)
class OrderReady:
    order_id: int