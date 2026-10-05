from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        "restaurant.Order",
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    menu_item = models.ForeignKey(
        "restaurant.MenuItem",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price_at_time = models.DecimalField()
    special_instructions = models.TextField(blank=True)
