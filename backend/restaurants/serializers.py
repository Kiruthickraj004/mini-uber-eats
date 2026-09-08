from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(
        source="owner.username"
    )

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "address",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]