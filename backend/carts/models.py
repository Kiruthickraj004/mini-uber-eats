from django.conf import settings
from django.db import models

from menus.models import MenuItem
from restaurants.models import Restaurant


class Cart(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CHECKED_OUT = "CHECKED_OUT", "Checked Out"
        ABANDONED = "ABANDONED", "Abandoned"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="carts",
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        related_name="carts",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer"],
                condition=models.Q(
                    status="ACTIVE"
                ),
                name="one_active_cart_per_customer",
            )
        ]

    def __str__(self):
        return f"Cart #{self.id} - {self.customer.username}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "menu_item"],
                name="unique_cart_menu_item",
            )
        ]

    def __str__(self):
        return (
            f"{self.menu_item.name} "
            f"x {self.quantity}"
        )