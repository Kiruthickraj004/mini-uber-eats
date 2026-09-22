from django.contrib import admin

from .models import Order, OrderItem, OutboxEvent


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "menu_item",
        "name_snapshot",
        "unit_price",
        "quantity",
        "subtotal",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "restaurant",
        "status",
        "assigned_driver_name",
        "subtotal",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "restaurant",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "restaurant__name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "customer",
        "restaurant",
        "assigned_driver_name",
        "subtotal",
        "created_at",
        "updated_at",
    )

    inlines = (
        OrderItemInline,
    )


@admin.register(OutboxEvent)
class OutboxEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event_type",
        "status",
        "attempts",
        "created_at",
        "processed_at",
        "updated_at",
    )

    list_filter = (
        "event_type",
        "status",
    )

    search_fields = (
        "event_type",
        "last_error",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "event_type",
        "payload",
        "status",
        "attempts",
        "last_error",
        "created_at",
        "processed_at",
        "updated_at",
    )