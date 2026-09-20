from django.db import transaction

from apps.restaurant.models import Order, OrderItem


@transaction.atomic
def create_order(*, customer, table_number, items):
    order = Order.objects.create(
        customer=customer, table_number=table_number, status=Order.status.PLACED
    )

    OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                menu_item=item["menu_item"],
                quantity=item["quantity"],
                unit_price_at_time=item["menu_item"].price,
                special_instructions=item.get("special_instructions", ""),
            )
            for item in items
        ]
    )

    return order
