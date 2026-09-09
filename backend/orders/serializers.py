from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "menu_item",
            "name_snapshot",
            "unit_price",
            "quantity",
            "subtotal",
        ]

        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):

    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True,
    )

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    payment_id = serializers.IntegerField(
    source="payment.id",
    read_only=True,
    )
    
    class Meta:
        model = Order

        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "status",
            "subtotal",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields