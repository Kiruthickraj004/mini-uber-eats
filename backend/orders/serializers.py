from rest_framework import serializers

from payments.serializers import PaymentSerializer

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

    customer_email = serializers.EmailField(
        source="customer.email",
        read_only=True,
    )

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    payment = PaymentSerializer(
        read_only=True,
    )

    payment_id = serializers.IntegerField(
        source="payment.id",
        read_only=True,
    )

    delivery_id = serializers.IntegerField(
        source="delivery.id",
        read_only=True,
        allow_null=True,
    )

    delivery_status = serializers.CharField(
        source="delivery.status",
        read_only=True,
        allow_null=True,
    )

    assigned_driver_id = serializers.IntegerField(
        source="delivery.driver.id",
        read_only=True,
        allow_null=True,
    )

    assigned_driver_name = serializers.SerializerMethodField()

    def get_assigned_driver_name(self, obj):
        delivery = getattr(obj, "delivery", None)
        driver = getattr(delivery, "driver", None)
        user = getattr(driver, "user", None)

        if user is None:
            return None

        return getattr(user, "username", None) or user.email

    class Meta:
        model = Order

        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "customer",
            "customer_email",
            "status",
            "subtotal",
            "items",
            "payment",
            "payment_id",
            "delivery_id",
            "delivery_status",
            "assigned_driver_id",
            "assigned_driver_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields