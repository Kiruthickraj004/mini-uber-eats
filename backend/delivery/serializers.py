from rest_framework import serializers

from .models import DriverProfile, DriverStatus


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