from django.conf import settings
from django.db import models


class Status(models.TextChoices):
    PLACED = "PLACED", "Placed"
    QUEUED = "QUEUED", "Queued"
    IN_PREP = "IN_PREP", "In Prep"
    READY = "READY", "Ready"
    SERVED = "SERVED", "Served"


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )
    table_number = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED,
    )

    placed_at = models.DateTimeField(auto_now_add=True)
    prep_started_at = models.DateTimeField(null=True, blank=True)
    estimated_ready_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    items = models.ManyToManyField(
        "restaurant.MenuItem",
        through="OrderItem",
        related_name="orders",
    )
