from django.contrib import admin

from .models import Payment, PaymentAttempt


class PaymentAttemptInline(admin.TabularInline):
    model = PaymentAttempt
    extra = 0

    readonly_fields = (
        "idempotency_key",
        "status",
        "provider_reference",
        "created_at",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "amount",
        "currency",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "order__customer__username",
        "order__customer__email",
        "order__restaurant__name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "order",
        "amount",
        "currency",
        "status",
        "created_at",
        "updated_at",
    )

    inlines = (
        PaymentAttemptInline,
    )


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payment",
        "status",
        "provider_reference",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "idempotency_key",
        "provider_reference",
        "payment__order__customer__username",
        "payment__order__customer__email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "payment",
        "idempotency_key",
        "status",
        "provider_reference",
        "created_at",
    )