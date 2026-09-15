try:
    from celery import shared_task  # type: ignore[reportMissingImports]
except ImportError:
    def shared_task(func):
        return func

from datetime import timedelta
from django.utils import timezone
from .models import Cart


@shared_task
def abandon_stale_carts():
    threshold = timezone.now() - timedelta(minutes=30)

    updated_count = (
        Cart.objects
        .filter(
            status=Cart.Status.ACTIVE,
            updated_at__lt=threshold,
        )
        .update(
            status=Cart.Status.ABANDONED,
            updated_at=timezone.now(),
        )
    )

    return {
        "abandoned_carts": updated_count,
    }