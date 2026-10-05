from rest_framework import serializers
from apps.restaurant.api.v1.serializers import OrderItemSerializer
from apps.restaurant.components import create_order
from apps.restaurant.models import Order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="order_items", many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "id",
            "customer",
            "status",
            "placed_at",
            "prep_started_at",
            "estimated_ready_at",
            "completed_at",
        ]

    def create(self, validated_data):
        return create_order(
            customer=self.context["request"].user,
            table_number=validated_data["table_number"],
            items=validated_data["order_items"],
        )
