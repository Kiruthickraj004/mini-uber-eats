from unittest.mock import patch
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import Cart, CartItem
from menus.models import MenuCategory, MenuItem
from orders.models import Order, OrderItem
from payments.models import Payment
from restaurants.models import Restaurant
from users.models import User


class CheckoutTests(APITestCase):

    def setUp(self):
        self.password = "StrongPassword123!"

        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password=self.password,
            role=User.Role.CUSTOMER,
        )

        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password=self.password,
            role=User.Role.RESTAURANT_OWNER,
        )

        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            name="Test Restaurant",
            description="Test",
            address="Test Address",
            status=Restaurant.Status.OPEN,
        )

        self.category = MenuCategory.objects.create(
            restaurant=self.restaurant,
            name="Main",
        )

        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name="Burger",
            description="Test burger",
            price=Decimal("250.00"),
            is_available=True,
        )

        self.cart = Cart.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            status=Cart.Status.ACTIVE,
        )

        CartItem.objects.create(
            cart=self.cart,
            menu_item=self.menu_item,
            quantity=2,
        )

        self.checkout_url = reverse(
            "order-checkout"
        )

        self.client.force_authenticate(
            user=self.customer
        )

    def test_checkout_creates_order_items_payment_and_closes_cart(
        self,
    ):
        response = self.client.post(
            self.checkout_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        order = Order.objects.get(
            customer=self.customer
        )

        self.assertEqual(
            order.restaurant,
            self.restaurant,
        )

        self.assertEqual(
            order.subtotal,
            Decimal("500.00"),
        )

        self.assertEqual(
            OrderItem.objects.filter(
                order=order
            ).count(),
            1,
        )

        order_item = OrderItem.objects.get(
            order=order
        )

        self.assertEqual(
            order_item.name_snapshot,
            "Burger",
        )

        self.assertEqual(
            order_item.unit_price,
            Decimal("250.00"),
        )

        self.assertEqual(
            order_item.quantity,
            2,
        )

        payment = Payment.objects.get(
            order=order
        )

        self.assertEqual(
            payment.amount,
            Decimal("500.00"),
        )

        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.status,
            Cart.Status.CHECKED_OUT,
        )

    def test_checkout_rejects_empty_cart(self):
        CartItem.objects.all().delete()

        response = self.client.post(
            self.checkout_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Order.objects.count(),
            0,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    def test_checkout_rejects_closed_restaurant(self):
        self.restaurant.status = (
            Restaurant.Status.CLOSED
        )
        self.restaurant.save()

        response = self.client.post(
            self.checkout_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(
            Order.objects.count(),
            0,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    def test_checkout_rejects_unavailable_item(self):
        self.menu_item.is_available = False
        self.menu_item.save()

        response = self.client.post(
            self.checkout_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(
            Order.objects.count(),
            0,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

    def test_checkout_uses_database_price(self):
        # Client doesn't submit a price.
        # Backend must use the current DB price.

        self.menu_item.price = Decimal(
            "300.00"
        )
        self.menu_item.save()

        response = self.client.post(
            self.checkout_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        order = Order.objects.get(
            customer=self.customer
        )

        self.assertEqual(
            order.subtotal,
            Decimal("600.00"),
        )

        order_item = OrderItem.objects.get(
            order=order
        )

        self.assertEqual(
            order_item.unit_price,
            Decimal("300.00"),
        )

    def test_checkout_rolls_back_if_payment_creation_fails(self):
        with patch(
            "orders.views.Payment.objects.create",
            side_effect=Exception(
                "Simulated payment creation failure"
            ),
        ):
            with self.assertRaises(Exception):
                self.client.post(
                    self.checkout_url
                )

        self.assertEqual(
            Order.objects.count(),
            0,
        )

        self.assertEqual(
            OrderItem.objects.count(),
            0,
        )

        self.assertEqual(
            Payment.objects.count(),
            0,
        )

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.status,
            Cart.Status.ACTIVE,
        )