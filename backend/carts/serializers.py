from decimal import Decimal

from rest_framework import serializers

from menus.models import MenuItem

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):

    menu_item_name = serializers.CharField(
        source="menu_item.name",
        read_only=True,
    )

    price = serializers.DecimalField(
        source="menu_item.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "menu_item",
            "menu_item_name",
            "price",
            "quantity",
            "subtotal",
        ]

        read_only_fields = [
            "id",
            "menu_item_name",
            "price",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.menu_item.price * obj.quantity


class AddCartItemSerializer(serializers.Serializer):

    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
    )

    quantity = serializers.IntegerField(
        min_value=1,
        max_value=50,
    )


class UpdateCartItemSerializer(serializers.Serializer):

    quantity = serializers.IntegerField(
        min_value=1,
        max_value=50,
    )


class CartSerializer(serializers.ModelSerializer):

    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True,
    )

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "status",
            "items",
            "subtotal",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields

    def get_subtotal(self, obj):
        return sum(
            (
                item.menu_item.price * item.quantity
                for item in obj.items.all()
            ),
            Decimal("0.00"),
        )