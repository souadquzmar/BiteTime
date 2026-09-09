from rest_framework.permissions import BasePermission
from apps.users.models import Role

class HasRole(BasePermission):
    allowed_roles =()

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles


class IsCustomer(HasRole):
    allowed_roles = (Role.CUSTOMER,)


class IsWaiter(HasRole):
    allowed_roles = (Role.WAITER,)

class IsChef(HasRole):
    allowed_roles = (Role.CHEF,)
