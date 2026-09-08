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

    class Meta:
        model = CartItem
        fields = [
            "id",
            "menu_item",
            "menu_item_name",
            "price",
            "quantity",
        ]


class AddCartItemSerializer(serializers.Serializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
    )

    quantity = serializers.IntegerField(
        min_value=1,
        max_value=50,
    )