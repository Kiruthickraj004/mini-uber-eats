from rest_framework import serializers

from .models import MenuCategory, MenuItem


class MenuCategorySerializer(
    serializers.ModelSerializer
):

    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True,
    )

    class Meta:
        model = MenuCategory

        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "name",
            "description",
            "display_order",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "restaurant_name",
            "created_at",
            "updated_at",
        ]


class MenuItemSerializer(
    serializers.ModelSerializer
):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    restaurant_name = serializers.CharField(
        source="category.restaurant.name",
        read_only=True,
    )

    class Meta:
        model = MenuItem

        fields = [
            "id",
            "category",
            "category_name",
            "restaurant_name",
            "name",
            "description",
            "price",
            "is_available",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "category_name",
            "restaurant_name",
            "created_at",
            "updated_at",
        ]