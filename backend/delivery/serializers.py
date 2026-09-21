from rest_framework import serializers

from .models import DriverProfile, DriverStatus, Delivery
from orders.models import Order

class DriverProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True,
    )

    class Meta:
        model = DriverProfile
        fields = [
            "id",
            "user_id",
            "status",
            "vehicle_type",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "created_at",
            "updated_at",
        ]

    def validate_status(self, value):
        if value == DriverStatus.BUSY:
            raise serializers.ValidationError(
                "BUSY status is managed by the delivery system."
            )

        return value



class DriverAvailableOrderSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "restaurant_name",
            "subtotal",
            "status",
            "created_at",
        ]


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            "id",
            "order",
            "driver",
            "status",
            "assigned_at",
            "picked_up_at",
            "delivered_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "order",
            "driver",
            "status",
            "assigned_at",
            "picked_up_at",
            "delivered_at",
            "updated_at",
        ]