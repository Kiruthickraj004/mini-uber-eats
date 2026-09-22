from django.contrib import admin

from .models import MenuCategory, MenuItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "restaurant",
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
        "restaurant",
    )

    search_fields = (
        "name",
        "restaurant__name",
    )

    ordering = (
        "restaurant",
        "display_order",
        "name",
    )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "get_restaurant",
        "price",
        "is_available",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_available",
        "category__restaurant",
    )

    search_fields = (
        "name",
        "category__name",
        "category__restaurant__name",
    )

    ordering = (
        "category__restaurant",
        "category",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(
        description="Restaurant",
        ordering="category__restaurant__name",
    )
    def get_restaurant(self, obj):
        return obj.category.restaurant.name