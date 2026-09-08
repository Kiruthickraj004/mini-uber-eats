from rest_framework.permissions import BasePermission

class isRestaurantResourceOwner(BasePermission):
    message = "You do not have permission to perform this action."

    def has_objectPermission(self, request, view, obj):
        return obj.owner == request.user