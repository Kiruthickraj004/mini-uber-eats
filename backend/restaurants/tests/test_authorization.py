from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurant
from users.models import User


class RestaurantAuthorizationTests(APITestCase):

    def setUp(self):
        self.password = "StrongPassword123!"

        self.owner_a = User.objects.create_user(
            username="owner_a",
            email="owner_a@example.com",
            password=self.password,
            role=User.Role.RESTAURANT_OWNER,
        )

        self.owner_b = User.objects.create_user(
            username="owner_b",
            email="owner_b@example.com",
            password=self.password,
            role=User.Role.RESTAURANT_OWNER,
        )

        self.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password=self.password,
            role=User.Role.CUSTOMER,
        )

        self.restaurant = Restaurant.objects.create(
            owner=self.owner_a,
            name="Owner A Restaurant",
            description="Test restaurant",
            address="Test Address",
            status=Restaurant.Status.OPEN,
        )

        self.list_url = reverse("restaurant-list")

        self.detail_url = reverse(
            "restaurant-detail",
            kwargs={"pk": self.restaurant.id},
        )

    def test_owner_can_access_own_restaurant(self):
        self.client.force_authenticate(
            user=self.owner_a
        )

        response = self.client.get(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_other_owner_cannot_access_restaurant(self):
        self.client.force_authenticate(
            user=self.owner_b
        )

        response = self.client.get(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_other_owner_cannot_update_restaurant(self):
        self.client.force_authenticate(
            user=self.owner_b
        )

        response = self.client.patch(
            self.detail_url,
            {
                "name": "Hacked Restaurant",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.restaurant.refresh_from_db()

        self.assertEqual(
            self.restaurant.name,
            "Owner A Restaurant",
        )

    def test_other_owner_cannot_delete_restaurant(self):
        self.client.force_authenticate(
            user=self.owner_b
        )

        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            Restaurant.objects.filter(
                id=self.restaurant.id
            ).exists()
        )

    def test_customer_cannot_modify_restaurant(self):
        self.client.force_authenticate(
            user=self.customer
        )

        response = self.client.patch(
            self.detail_url,
            {
                "name": "Customer Hacked Restaurant",
            },
            format="json",
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            ],
        )

        self.restaurant.refresh_from_db()

        self.assertEqual(
            self.restaurant.name,
            "Owner A Restaurant",
        )