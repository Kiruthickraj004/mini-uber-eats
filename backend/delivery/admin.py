from django.contrib import admin

from .models import DriverProfile, Delivery


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "vehicle_type",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "vehicle_type",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "driver",
        "status",
        "assigned_at",
        "picked_up_at",
        "delivered_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "driver",
        "assigned_at",
    )

    search_fields = (
        "driver__user__username",
        "driver__user__email",
        "order__customer__username",
        "order__customer__email",
    )

    ordering = ("-assigned_at",)

    readonly_fields = (
        "order",
        "driver",
        "status",
        "assigned_at",
        "picked_up_at",
        "delivered_at",
        "updated_at",
    )