from django.core.management.base import BaseCommand

from apps.restaurant.components.kitchen_capacity import KitchenCapacity


class Command(BaseCommand):
    help = "Calculate the current kitchen workload."

    def handle(self, *args, **options):
        capacity = KitchenCapacity.calculate()

        self.stdout.write(
            self.style.SUCCESS("Kitchen capacity calculated successfully.")
        )

        self.stdout.write(f"Queued orders: {capacity['queued_orders']}")

        self.stdout.write(f"In-prep orders: {capacity['in_prep_orders']}")

        self.stdout.write(f"Total active orders: {capacity['total_active_orders']}")

        self.stdout.write(
            f"Queued workload: " f"{capacity['queued_workload_minutes']} minutes"
        )

        self.stdout.write(
            f"In-prep workload: " f"{capacity['in_prep_workload_minutes']} minutes"
        )

        self.stdout.write(
            f"Total workload: " f"{capacity['total_workload_minutes']} minutes"
        )
