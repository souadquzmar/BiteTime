from apps.restaurant.models import Order


class PrepEstimator:
    @staticmethod
    def calculate(order):
        max_prep_time = 0
        for item in order.order_items.select_related("menu_item").all():
            max_prep_time = max(max_prep_time, item.menu_item.estimated_prep_minutes)

        queue_backlog = 0

        queued_orders = (
            Order.objects.filter(status=Order.status.QUEUED)
            .exclude(pk=order.pk)
            .prefetch_related("order_items__menu_item")
        )

        for queued_order in queued_orders:
            order_max_prep = 0

            for item in queued_order.order_items.all():
                order_max_prep = max(
                    order_max_prep,
                    item.menu_item.estimated_prep_minutes,
                )

            queue_backlog += order_max_prep

        return max_prep_time + queue_backlog
