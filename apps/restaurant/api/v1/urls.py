from django.urls import path

from apps.restaurant.api.v1.views import MenuItemView

urlpatterns = [
    path("menu/", MenuItemView.as_view(), name="menu"),
]
