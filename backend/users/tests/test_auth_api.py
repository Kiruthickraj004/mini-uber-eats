from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthenticationAPITests(APITestCase):

    def setUp(self):
        self.register_url = reverse("user-register")
        self.token_url = reverse("token_obtain_pair")
        self.me_url = reverse("user-me")

        self.password = "StrongPassword123!"

        self.user = User.objects.create_user(
            username="customer1",
            email="customer1@example.com",
            password=self.password,
            role=User.Role.CUSTOMER,
        )

    def test_user_can_register(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "customer2",
                "email": "customer2@example.com",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(
            username="customer2"
        )

        self.assertEqual(
            user.role,
            User.Role.CUSTOMER,
        )

    def test_registration_cannot_choose_privileged_role(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "attacker",
                "email": "attacker@example.com",
                "password": self.password,
                "role": User.Role.RESTAURANT_OWNER,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(
            username="attacker"
        )

        self.assertEqual(
            user.role,
            User.Role.CUSTOMER,
        )

    def test_user_can_login(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "customer1",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login_fails(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "customer1",
                "password": "WrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me_requires_authentication(self):
        response = self.client.get(
            self.me_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_access_me(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            self.me_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            self.user.email,
        )