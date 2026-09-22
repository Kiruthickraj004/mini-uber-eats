from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "recipient",
        "notification_type",
        "channel",
        "status",
        "attempts",
        "sent_at",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "channel",
        "status",
        "created_at",
    )

    search_fields = (
        "recipient__username",
        "recipient__email",
        "order__id",
        "last_error",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "order",
        "recipient",
        "notification_type",
        "channel",
        "status",
        "attempts",
        "last_error",
        "sent_at",
        "created_at",
        "updated_at",
    )