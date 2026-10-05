from rest_framework import serializers

from apps.restaurant.models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = "__all__"
