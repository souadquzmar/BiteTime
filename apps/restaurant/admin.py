from django.contrib import admin
from apps.restaurant.models import MenuItem, Order, OrderItem
from apps.users.models import User

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
