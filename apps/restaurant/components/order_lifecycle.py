from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.restaurant.components import PrepEstimator
from apps.restaurant.models import Order
from apps.restaurant.models.order import Status
from services import OrderEmailService


class OrderLifecycle:
    @staticmethod
    def queue(order):
        if order.status != Status.PLACED:
            raise ValidationError("only placed orders can be queues")
        order.status = Status.QUEUED
        order.save(update_fields=["status"])

        return order

    @staticmethod
    def start_prep(order):
        if order.status != Status.QUEUED:
            raise ValidationError("only queued orders can start prep")

        now = timezone.now()
        prep_time = PrepEstimator.calculate(order)
        order.status = Status.IN_PREP
        order.prep_started_at = now
        order.estimated_ready_at = now + timedelta(minutes=prep_time)
        order.save(update_fields=["status", "prep_started_at", "estimated_ready_at"])

        OrderEmailService.send_started(order)

        return order

    @staticmethod
    def mark_ready(order):
        if order.status != Status.IN_PREP:
            raise ValidationError("only orders in preparation can be marked ready")

        order.status = Status.READY
        order.completed_at = timezone.now()
        order.save(update_fields=["status", "completed_at"])

        OrderEmailService.send_ready(order)

        return order
