from apps.restaurant.models import Order
from apps.restaurant.models.order import Status


class KitchenCapacity:

    @staticmethod
    def calculate():
        queued_orders = Order.objects.filter(
            status=Status.QUEUED,
        )

        in_prep_orders = Order.objects.filter(
            status=Status.IN_PREP,
        )

        queued_workload = 0

        for order in queued_orders:
            queued_workload += KitchenCapacity._order_prep_time(order)

        in_prep_workload = 0

        for order in in_prep_orders:
            in_prep_workload += KitchenCapacity._order_prep_time(order)

        return {
            "queued_orders": queued_orders.count(),
            "in_prep_orders": in_prep_orders.count(),
            "total_active_orders": (queued_orders.count() + in_prep_orders.count()),
            "queued_workload_minutes": queued_workload,
            "in_prep_workload_minutes": in_prep_workload,
            "total_workload_minutes": (queued_workload + in_prep_workload),
        }

    @staticmethod
    def _order_prep_time(order):
        max_prep_time = 0

        for item in order.order_items.select_related("menu_item").all():
            max_prep_time = max(
                max_prep_time,
                item.menu_item.estimated_prep_minutes,
            )

        return max_prep_time
