from django.urls import path

from apps.restaurant.api.v1.views import MenuItemView, OrderView

urlpatterns = [
    path("menu/", MenuItemView.as_view(), name="menu"),
    path("order/", OrderView.as_view(), name="order"),
]
