from rest_framework import serializers

from apps.restaurant.models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    model = MenuItem

    class Meta:
        fields = "__all__"
