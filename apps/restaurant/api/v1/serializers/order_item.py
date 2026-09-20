from rest_framework import serializers

from apps.restaurant.models import OrderItem, MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.filter(is_available=True)
    )

    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity", "special_instructions"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value
