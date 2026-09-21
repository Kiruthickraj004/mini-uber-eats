from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone
from orders.tasks import (process_outbox_events,recover_stuck_outbox_events)

from orders.models import Order, OutboxEvent
from payments.models import Payment
from restaurants.models import Restaurant
from users.models import User
from orders.tasks import process_outbox_events

class OutboxTests(APITestCase):

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
            status=Order.Status.PREPARING,
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

    def test_marking_order_ready_creates_outbox_event(self):
        url = reverse(
            "order-ready",
            kwargs={
                "pk": self.order.id,
            },
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.Status.READY,
        )

        event = OutboxEvent.objects.get(
            event_type=OutboxEvent.EventType.ORDER_READY
        )

        self.assertEqual(
            event.payload["order_id"],
            self.order.id,
        )

        self.assertEqual(
            event.status,
            OutboxEvent.Status.PENDING,
        )

    def test_only_one_order_ready_event_is_created(self):
        url = reverse(
            "order-ready",
            kwargs={
                "pk": self.order.id,
            },
        )

        self.client.post(url)

        # The order is now READY, so attempting
        # to mark it READY again must fail.
        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertEqual(
            OutboxEvent.objects.filter(
                event_type=OutboxEvent.EventType.ORDER_READY
            ).count(),
            1,
        )

    @patch("orders.tasks.dispatch")
    def test_dispatcher_processes_pending_event(
        self,
        mock_dispatch,
    ):
        event = OutboxEvent.objects.create(
            event_type=OutboxEvent.EventType.ORDER_READY,
            payload={
                "order_id": self.order.id,
            },
        )

        result = process_outbox_events()

        event.refresh_from_db()

        self.assertEqual(
            event.status,
            OutboxEvent.Status.PROCESSED,
        )

        self.assertIsNotNone(
            event.processed_at
        )

        mock_dispatch.assert_called_once()

        self.assertEqual(
            result["processed"],
            1,
        )

    def test_stuck_processing_event_is_recovered(self):
        event = OutboxEvent.objects.create(
            event_type=OutboxEvent.EventType.ORDER_READY,
            payload={
                "order_id": self.order.id,
            },
            status=OutboxEvent.Status.PROCESSING,
            attempts=1,
        )

        OutboxEvent.objects.filter(
            id=event.id
        ).update(
            updated_at=(
                timezone.now()
                - timedelta(minutes=20)
            )
        )

        result = recover_stuck_outbox_events()

        event.refresh_from_db()

        self.assertEqual(
            event.status,
            OutboxEvent.Status.PENDING,
        )

        self.assertEqual(
            result["recovered"],
            1,
        )