from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from users.models import User
from users.permissions import IsDriver
from orders.models import Order

from .models import DriverProfile, DriverStatus, Delivery, DeliveryStatus
from .serializers import DriverProfileSerializer, DriverAvailableOrderSerializer, DeliverySerializer


class DriverProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.DRIVER:
            return Response(
                {
                    "code": "DRIVER_ONLY",
                    "detail": "Only drivers can access a driver profile.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        profile = DriverProfile.objects.filter(
            user=request.user
        ).first()

        if profile is None:
            return Response(
                {
                    "code": "DRIVER_PROFILE_NOT_FOUND",
                    "detail": "Driver profile does not exist.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            DriverProfileSerializer(profile).data
        )

    def post(self, request):
        if request.user.role != User.Role.DRIVER:
            return Response(
                {
                    "code": "DRIVER_ONLY",
                    "detail": "Only drivers can create a driver profile.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if DriverProfile.objects.filter(
            user=request.user
        ).exists():
            return Response(
                {
                    "code": "DRIVER_PROFILE_EXISTS",
                    "detail": "Driver profile already exists.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        serializer = DriverProfileSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            profile = serializer.save(user=request.user)
        except IntegrityError:
            return Response(
                {
                    "code": "DRIVER_PROFILE_EXISTS",
                    "detail": "Driver profile already exists.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            DriverProfileSerializer(profile).data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request):
        if request.user.role != User.Role.DRIVER:
            return Response(
                {
                    "code": "DRIVER_ONLY",
                    "detail": "Only drivers can update a driver profile.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        profile = DriverProfile.objects.filter(
            user=request.user
        ).first()

        if profile is None:
            return Response(
                {
                    "code": "DRIVER_PROFILE_NOT_FOUND",
                    "detail": "Driver profile does not exist.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DriverProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data
        )

class ClaimDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        if not hasattr(request.user, "driver_profile"):
            return Response(
                {
                    "code": "DRIVER_ONLY",
                    "detail": "Only drivers can claim deliveries.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            with transaction.atomic():
                order = (
                    Order.objects
                    .select_for_update()
                    .select_related("restaurant")
                    .filter(id=order_id)
                    .first()
                )

                if order is None:
                    return Response(
                        {
                            "code": "ORDER_NOT_FOUND",
                            "detail": "Order not found.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                if order.status != Order.Status.READY:
                    return Response(
                        {
                            "code": "ORDER_NOT_READY",
                            "detail": "Only READY orders can be claimed.",
                        },
                        status=status.HTTP_409_CONFLICT,
                    )

                driver = (
                    DriverProfile.objects
                    .select_for_update()
                    .filter(user=request.user)
                    .first()
                )

                if driver is None:
                    return Response(
                        {
                            "code": "DRIVER_PROFILE_NOT_FOUND",
                            "detail": "Driver profile not found.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                if driver.status != DriverStatus.AVAILABLE:
                    return Response(
                        {
                            "code": "DRIVER_NOT_AVAILABLE",
                            "detail": "Driver is not available.",
                        },
                        status=status.HTTP_409_CONFLICT,
                    )

                if Delivery.objects.filter(order=order).exists():
                    return Response(
                        {
                            "code": "DELIVERY_ALREADY_ASSIGNED",
                            "detail": "This order is already assigned.",
                        },
                        status=status.HTTP_409_CONFLICT,
                    )

                delivery = Delivery.objects.create(
                    order=order,
                    driver=driver,
                    status=DeliveryStatus.ASSIGNED,
                )

                order.status = Order.Status.DRIVER_ASSIGNED
                order.save(
                    update_fields=["status", "updated_at"]
                )

                driver.status = DriverStatus.BUSY
                driver.save(
                    update_fields=["status", "updated_at"]
                )

                return Response(
                    {
                        "delivery_id": delivery.id,
                        "order_id": order.id,
                        "driver_id": driver.id,
                        "status": delivery.status,
                    },
                    status=status.HTTP_201_CREATED,
                )

        except IntegrityError:
            return Response(
                {
                    "code": "DELIVERY_ALREADY_ASSIGNED",
                    "detail": "This order is already assigned.",
                },
                status=status.HTTP_409_CONFLICT,
            )

class PickupDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, delivery_id):
        with transaction.atomic():
            delivery = (
                Delivery.objects
                .select_for_update()
                .select_related("order", "driver")
                .filter(
                    id=delivery_id,
                    driver__user=request.user,
                )
                .first()
            )

            if delivery is None:
                return Response(
                    {
                        "code": "DELIVERY_NOT_FOUND",
                        "detail": "Delivery not found.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if delivery.status != DeliveryStatus.ASSIGNED:
                return Response(
                    {
                        "code": "INVALID_DELIVERY_STATE",
                        "detail": "Only assigned deliveries can be picked up.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            if delivery.order.status != Order.Status.DRIVER_ASSIGNED:
                return Response(
                    {
                        "code": "INVALID_ORDER_STATE",
                        "detail": "Order is not ready for pickup.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            delivery.status = DeliveryStatus.PICKED_UP
            delivery.picked_up_at = timezone.now()
            delivery.save(
                update_fields=[
                    "status",
                    "picked_up_at",
                    "updated_at",
                ]
            )

            delivery.order.status = Order.Status.PICKED_UP
            delivery.order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            return Response({
                "delivery_id": delivery.id,
                "order_id": delivery.order.id,
                "status": delivery.status,
                "picked_up_at": delivery.picked_up_at,
            })

class CompleteDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, delivery_id):
        with transaction.atomic():
            delivery = (
                Delivery.objects
                .select_for_update()
                .select_related("order", "driver")
                .filter(
                    id=delivery_id,
                    driver__user=request.user,
                )
                .first()
            )

            if delivery is None:
                return Response(
                    {
                        "code": "DELIVERY_NOT_FOUND",
                        "detail": "Delivery not found.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if delivery.status != DeliveryStatus.PICKED_UP:
                return Response(
                    {
                        "code": "INVALID_DELIVERY_STATE",
                        "detail": "Only picked-up deliveries can be completed.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            if delivery.order.status != Order.Status.PICKED_UP:
                return Response(
                    {
                        "code": "INVALID_ORDER_STATE",
                        "detail": "Order is not ready for delivery completion.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            delivery.status = DeliveryStatus.DELIVERED
            delivery.delivered_at = timezone.now()
            delivery.save(
                update_fields=[
                    "status",
                    "delivered_at",
                    "updated_at",
                ]
            )

            delivery.order.status = Order.Status.DELIVERED
            delivery.order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            delivery.driver.status = DriverStatus.AVAILABLE
            delivery.driver.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            return Response({
                "delivery_id": delivery.id,
                "order_id": delivery.order.id,
                "status": delivery.status,
                "delivered_at": delivery.delivered_at,
            })



class AvailableOrdersView(ListAPIView):
    serializer_class = DriverAvailableOrderSerializer
    permission_classes = [
        IsAuthenticated,
        IsDriver,
    ]

    def get_queryset(self):
        return (
            Order.objects
            .select_related("restaurant")
            .filter(
                status=Order.Status.READY,
            )
            .order_by("created_at")
        )


class MyDeliveriesView(ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [
        IsAuthenticated,
        IsDriver,
    ]

    def get_queryset(self):
        return (
            Delivery.objects
            .select_related(
                "order",
                "order__restaurant",
                "driver",
            )
            .filter(
                driver__user=self.request.user,
            )
            .order_by("-assigned_at")
        )