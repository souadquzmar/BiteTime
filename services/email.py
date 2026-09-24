from django.core.mail import send_mail
from django.conf import settings


class OrderEmailService:
    @staticmethod
    def send_started(order):
        send_mail(
            subject=f"Order #{order.id} is being prepared",
            message=(
                f"Your order #{order.id} is now being prepared.\n"
                f"Estimated ready time: {order.estimated_ready_at}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
        )

    @staticmethod
    def send_ready(order):
        send_mail(
            subject=f"Order #{order.id} is ready",
            message=(f"Your order #{order.id} is ready."),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
        )
