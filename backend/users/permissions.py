from rest_framework.permissions import BasePermission
from .models import User

class IsRestaurantOwner(BasePermission):
    message = "You must be the owner of the restaurant to perform this action."

    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == User.Role.RESTAURANT_OWNER


class IsCustomer(BasePermission):
    message = "You must be a customer to perform this action."

    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role == User.Role.CUSTOMER