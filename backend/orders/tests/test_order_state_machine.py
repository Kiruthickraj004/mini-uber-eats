from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order
from payments.models import Payment
from restaurants.models import Restaurant
from users.models import User


class OrderStateMachineTests(APITestCase):

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

        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            subtotal=Decimal("500.00"),
            status=Order.Status.PENDING,
        )

        self.payment = Payment.objects.create(
            order=self.order,
            amount=Decimal("500.00"),
            currency="INR",
            status=Payment.Status.SUCCESS,
        )

        self.client.force_authenticate(
            user=self.owner
        )

    def post_action(
        self,
        url_name,
    ):
        url = reverse(
            url_name,
            kwargs={
                "pk": self.order.id,
            },
        )

        return self.client.post(url)

    def test_pending_can_be_confirmed(self):
        response = self.post_action(
            "order-accept"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.CONFIRMED,
        )

    def test_pending_can_be_rejected(self):
        response = self.post_action(
            "order-reject"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.REJECTED,
        )

    def test_pending_cannot_jump_to_ready(self):
        response = self.post_action(
            "order-ready"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.PENDING,
        )

    def test_confirmed_can_start_preparing(self):
        self.order.status = (
            Order.Status.CONFIRMED
        )
        self.order.save()

        response = self.post_action(
            "order-start-preparing"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.PREPARING,
        )

    def test_confirmed_cannot_be_marked_ready_directly(self):
        self.order.status = (
            Order.Status.CONFIRMED
        )
        self.order.save()

        response = self.post_action(
            "order-ready"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.CONFIRMED,
        )

    def test_preparing_can_be_marked_ready(self):
        self.order.status = (
            Order.Status.PREPARING
        )
        self.order.save()

        response = self.post_action(
            "order-ready"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.READY,
        )

    def test_rejected_order_cannot_be_prepared(self):
        self.order.status = (
            Order.Status.REJECTED
        )
        self.order.save()

        response = self.post_action(
            "order-start-preparing"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.REJECTED,
        )

    def test_delivered_order_cannot_move_backward(self):
        self.order.status = (
            Order.Status.DELIVERED
        )
        self.order.save()

        response = self.post_action(
            "order-accept"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.DELIVERED,
        )

    def test_pending_payment_cannot_be_accepted(self):
        self.payment.status = (
            Payment.Status.PENDING
        )
        self.payment.save()

        response = self.post_action(
            "order-accept"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(
            response.data["code"],
            "PAYMENT_REQUIRED",
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.PENDING,
        )