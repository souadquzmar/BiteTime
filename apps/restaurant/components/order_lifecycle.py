from rest_framework.exceptions import ValidationError

from apps.restaurant.models import Order


class OrderLifecycle:
    @staticmethod
    def queue(order):
        if order.status != Order.status.PLACED:
            raise ValidationError("only placed orders can be queues")
        order.status = Order.status.QUEUED
        order.save(updated_fields=["status"])

        return order
