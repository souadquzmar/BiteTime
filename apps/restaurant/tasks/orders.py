from celery import shared_task
from django.utils import timezone

from apps.restaurant.components.order_lifecycle import OrderLifecycle
from apps.restaurant.models import Order
from apps.restaurant.models.order import Status


@shared_task
def process_ready_orders():
    now = timezone.now()

    orders = Order.objects.filter(
        status=Status.IN_PREP,
        estimated_ready_at__isnull=False,
        estimated_ready_at__lte=now,
    )

    processed_count = 0

    for order in orders:
        OrderLifecycle.mark_ready(order)
        processed_count += 1

    return {"processed_orders": processed_count}
