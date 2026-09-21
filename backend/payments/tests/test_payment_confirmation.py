from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import Cart
from menus.models import MenuCategory, MenuItem
from orders.models import Order
from payments.models import Payment, PaymentAttempt
from restaurants.models import Restaurant
from users.models import User
import threading
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache
from django.test import TransactionTestCase

class PaymentConfirmationTests(APITestCase):

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
            price=Decimal("250.00"),
            is_available=True,
        )

        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            subtotal=Decimal("250.00"),
            status=Order.Status.PENDING,
        )

        self.payment = Payment.objects.create(
            order=self.order,
            amount=Decimal("250.00"),
            currency="INR",
            status=Payment.Status.PENDING,
        )

        self.confirm_url = reverse(
            "payment-confirm",
            kwargs={
                "pk": self.payment.id,
            },
        )

        self.client.force_authenticate(
            user=self.customer
        )

    def test_confirmation_requires_idempotency_key(self):
        response = self.client.post(
            self.confirm_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            PaymentAttempt.objects.count(),
            0,
        )

    def test_payment_confirmation_succeeds(self):
        response = self.client.post(
            self.confirm_url,
            HTTP_IDEMPOTENCY_KEY="payment-test-1",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )

        self.assertEqual(
            PaymentAttempt.objects.count(),
            1,
        )

    def test_same_idempotency_key_does_not_create_second_attempt(
        self,
    ):
        idempotency_key = "payment-test-duplicate"

        first_response = self.client.post(
            self.confirm_url,
            HTTP_IDEMPOTENCY_KEY=idempotency_key,
        )

        second_response = self.client.post(
            self.confirm_url,
            HTTP_IDEMPOTENCY_KEY=idempotency_key,
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            PaymentAttempt.objects.count(),
            1,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )

    def test_successful_payment_with_different_key_does_not_process_again(
        self,
    ):
        first_response = self.client.post(
            self.confirm_url,
            HTTP_IDEMPOTENCY_KEY="payment-key-1",
        )

        second_response = self.client.post(
            self.confirm_url,
            HTTP_IDEMPOTENCY_KEY="payment-key-2",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            PaymentAttempt.objects.count(),
            1,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )


class PaymentConcurrencyTests(TransactionTestCase):

    reset_sequences = True

    def setUp(self):
        self.password = "StrongPassword123!"

        self.customer = User.objects.create_user(
            username="concurrent_customer",
            email="concurrent@example.com",
            password=self.password,
            role=User.Role.CUSTOMER,
        )

        self.owner = User.objects.create_user(
            username="concurrent_owner",
            email="owner@example.com",
            password=self.password,
            role=User.Role.RESTAURANT_OWNER,
        )

        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            name="Concurrent Restaurant",
            address="Test Address",
            status=Restaurant.Status.OPEN,
        )

        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            subtotal=Decimal("250.00"),
            status=Order.Status.PENDING,
        )

        self.payment = Payment.objects.create(
            order=self.order,
            amount=Decimal("250.00"),
            currency="INR",
            status=Payment.Status.PENDING,
        )

    def test_concurrent_confirmation_creates_only_one_attempt(
        self,
    ):
        def confirm_payment():
            from rest_framework.test import APIClient

            client = APIClient()

            client.force_authenticate(
                user=self.customer
            )

            return client.post(
                reverse(
                    "payment-confirm",
                    kwargs={
                        "pk": self.payment.id,
                    },
                ),
                HTTP_IDEMPOTENCY_KEY=(
                    f"concurrent-{threading.get_ident()}"
                ),
            )

        with ThreadPoolExecutor(
            max_workers=5
        ) as executor:

            responses = list(
                executor.map(
                    lambda _: confirm_payment(),
                    range(5),
                )
            )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            Payment.Status.SUCCESS,
        )

        self.assertEqual(
            PaymentAttempt.objects.filter(
                payment=self.payment
            ).count(),
            1,
        )

        self.assertTrue(
            any(
                response.status_code
                == 200
                for response in responses
            )
        )