from celery import chain, group, chord  # pyright: ignore[reportMissingImports]
from .tasks import notify_order_ready, record_notification_completion, notify_driver, process_driver_notification_results
from delivery.models import DriverProfile

def order_ready_notification_workflow(notification_id):
    workflow = chain(
        notify_order_ready.s(notification_id),
        record_notification_completion.s(),
    )

    return workflow.delay(notification_id)


def notify_drivers_workflow(order_id, driver_ids):
    workflow = group(
        notify_driver.s(driver_id, order_id)
        for driver_id in driver_ids
    )

    return workflow.delay()

def notify_available_drivers_workflow(order_id):
    driver_ids = list(
        DriverProfile.objects
        .filter(status=DriverProfile.Status.AVAILABLE)
        .values_list("id", flat=True)
    )

    if not driver_ids:
        return None

    workflow = chord(
        notify_driver.s(driver_id, order_id)
        for driver_id in driver_ids
    )(
        process_driver_notification_results.s()
    )

    return workflow