from rest_framework import generics

from apps.restaurant.api.v1.serializers import OrderSerializer
from apps.restaurant.models import Order
from apps.users.api.v1.permissions.role_permissions import IsCustomer


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]
