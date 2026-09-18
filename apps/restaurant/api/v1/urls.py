from django.urls import path

from apps.restaurant.api.v1.views import (
    MenuItemView,
    OrderView,
    QueueOrderView,
    StartOrderPrepView,
    MarkOrderReadyView,
)

urlpatterns = [
    path("menu/", MenuItemView.as_view(), name="menu"),
    path("orders/", OrderView.as_view(), name="orders"),
    path("orders/<int:pk>/queue/", QueueOrderView.as_view(), name="order-queue"),
    path(
        "orders/<int:pk>/start-prep/",
        StartOrderPrepView.as_view(),
        name="start-order-prep",
    ),
    path(
        "orders/<int:pk>/mark-ready/",
        MarkOrderReadyView.as_view(),
        name="mark-order-ready",
    ),
]
