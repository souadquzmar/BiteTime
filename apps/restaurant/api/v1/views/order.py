from rest_framework import generics
from apps.restaurant.api.v1.serializers import OrderSerializer
from apps.restaurant.components import OrderLifecycle
from apps.restaurant.models import Order
from apps.users.api.v1.permissions.role_permissions import IsCustomer, IsWaiter, IsChef
from core.response import success_response


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]


class QueueOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsWaiter]
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        order = generics.get_object_or_404(Order, pk=kwargs["pk"])

        order = OrderLifecycle.queue(order=order)

        return success_response(
            message="Order queued successfully", data=OrderSerializer(order).data
        )


class StartOrderPrepView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsChef]
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        order = generics.get_object_or_404(Order, pk=kwargs["pk"])

        order = OrderLifecycle.start_prep(order=order)

        return success_response(
            message="Order started preparation successfully",
            data=OrderSerializer(order).data,
        )
