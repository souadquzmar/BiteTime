from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.menu.api.v1.serializers import MenuItemSerializer
from apps.menu.models import MenuItem


class MenuItemView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
