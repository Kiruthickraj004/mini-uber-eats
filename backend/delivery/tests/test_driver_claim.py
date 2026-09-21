from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from django.test import TransactionTestCase
from django.urls import reverse

from rest_framework.test import APIClient

from delivery.models import Delivery, DriverProfile
from orders.models import Order
from restaurants.models import Restaurant
from users.models import User


class DriverClaimConcurrencyTests(
    TransactionTestCase
):

    reset_sequences = True

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

        self.drivers = []

        for index in range(3):
            driver_user = User.objects.create_user(
                username=f"driver{index}",
                email=f"driver{index}@example.com",
                password=self.password,
                role=User.Role.DRIVER,
            )

            profile = DriverProfile.objects.create(
                user=driver_user,
                status=DriverProfile.Status.AVAILABLE,
                vehicle_type="BIKE",
            )

            self.drivers.append(profile)

        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            name="Test Restaurant",
            address="Test Address",
            status=Restaurant.Status.OPEN,
        )

        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            subtotal=Decimal("500.00"),
            status=Order.Status.READY,
        )

    def claim_order(self, driver):
        client = APIClient()

        client.force_authenticate(
            user=driver.user
        )

        url = reverse(
            "delivery-claim-order",
            kwargs={
                "order_id": self.order.id,
            },
        )

        return client.post(url)

    def test_only_one_driver_can_claim_order(self):
        with ThreadPoolExecutor(
            max_workers=3
        ) as executor:

            responses = list(
                executor.map(
                    self.claim_order,
                    self.drivers,
                )
            )

        successful = [
            response
            for response in responses
            if response.status_code
            in (200, 201)
        ]

        conflicts = [
            response
            for response in responses
            if response.status_code == 409
        ]

        self.assertEqual(
            len(successful),
            1,
        )

        self.assertEqual(
            len(conflicts),
            2,
        )

        self.assertEqual(
            Delivery.objects.filter(
                order=self.order
            ).count(),
            1,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.DRIVER_ASSIGNED,
        )

        self.assertEqual(
            DriverProfile.objects.filter(
                status=DriverProfile.Status.BUSY
            ).count(),
            1,
        )

        self.assertEqual(
            DriverProfile.objects.filter(
                status=DriverProfile.Status.AVAILABLE
            ).count(),
            2,
        )