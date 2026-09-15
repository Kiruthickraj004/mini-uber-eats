from importlib import import_module
try:
    shared_task = import_module("celery").shared_task
except ImportError:
    def shared_task(func):
        return func
from django.db import transaction
from django.utils import timezone
from .events import OrderReady
from .models import OutboxEvent
from config.events import dispatch
from datetime import timedelta

@shared_task
def process_outbox_events():
    processed_count = 0

    events = (
        OutboxEvent.objects
        .filter(status=OutboxEvent.Status.PENDING)
        .order_by("created_at")[:100]
    )

    for event in events:
        try:
            with transaction.atomic():
                locked_event = (
                    OutboxEvent.objects
                    .select_for_update()
                    .get(id=event.id)
                )

                if locked_event.status != OutboxEvent.Status.PENDING:
                    continue

                locked_event.status = OutboxEvent.Status.PROCESSING
                locked_event.attempts += 1
                locked_event.save(
                    update_fields=[
                        "status",
                        "attempts",
                        "updated_at",
                    ]
                )

                if locked_event.event_type == OutboxEvent.EventType.ORDER_READY:
                    dispatch(
                        OrderReady(
                            order_id=locked_event.payload["order_id"]
                        )
                    )

                locked_event.status = OutboxEvent.Status.PROCESSED
                locked_event.processed_at = timezone.now()
                locked_event.save(
                    update_fields=[
                        "status",
                        "processed_at",
                        "updated_at",
                    ]
                )

                processed_count += 1

        except Exception as exc:
            OutboxEvent.objects.filter(
                id=event.id
            ).update(
                status=OutboxEvent.Status.FAILED,
                last_error=str(exc),
            )

    return {
        "processed": processed_count,
    }


@shared_task
def recover_stuck_outbox_events():
    threshold = timezone.now() - timedelta(minutes=10)

    recovered_count = (
        OutboxEvent.objects
        .filter(
            status=OutboxEvent.Status.PROCESSING,
            updated_at__lt=threshold,
        )
        .update(
            status=OutboxEvent.Status.PENDING,
            last_error="Recovered from stale PROCESSING state.",
        )
    )

    return {
        "recovered": recovered_count,
    }