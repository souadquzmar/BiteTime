from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.restaurant.components import PrepEstimator
from apps.restaurant.models import Order


class OrderLifecycle:
    @staticmethod
    def queue(order):
        if order.status != Order.status.PLACED:
            raise ValidationError("only placed orders can be queues")
        order.status = Order.status.QUEUED
        order.save(updated_fields=["status"])

        return order

    @staticmethod
    def start_prep(order):
        if order.status != Order.status.QUEUED:
            raise ValidationError("only queued orders can start prep")

        now = timezone.now()
        prep_time = PrepEstimator.calculate(order)
        order.status = Order.status.IN_PREP
        order.prep_started_at = now
        order.estimated_ready_at = now + timedelta(minutes=prep_time)
        order.save(updated_fields=["status", "prep_started_at", "estimated_ready_at"])

        return order

    @staticmethod
    def mark_ready(order):
        if order.status != Order.status.IN_PREP:
            raise ValidationError("only orders in preparation can be marked ready")

        order.status = Order.status.READY
        order.completed_at = timezone.now()
        order.save(updated_fields=["status", "completed_at"])

        return order
