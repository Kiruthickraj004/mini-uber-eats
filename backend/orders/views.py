from decimal import Decimal

from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from payments.models import Payment, PaymentStatus
from carts.models import Cart
from users.permissions import IsCustomer, IsRestaurantOwner

from .models import Order, OrderItem, OutboxEvent
from .serializers import OrderSerializer

from config.events import dispatch
from .events import OrderReady


class CheckoutView(APIView):

    permission_classes = [IsCustomer]

    def post(self, request):

        with transaction.atomic():

            cart = (
                Cart.objects
                .select_for_update()
                .select_related("restaurant")
                .prefetch_related(
                    "items__menu_item__category__restaurant"
                )
                .filter(
                    customer=request.user,
                    status=Cart.Status.ACTIVE,
                )
                .first()
            )

            if cart is None:
                return Response(
                    {
                        "error": "ACTIVE_CART_NOT_FOUND",
                        "message": "You do not have an active cart.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            cart_items = list(cart.items.all())

            if not cart_items:
                return Response(
                    {
                        "error": "EMPTY_CART",
                        "message": "Your cart is empty.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            if cart.restaurant.status != cart.restaurant.Status.OPEN:
                return Response(
                    {
                        "error": "RESTAURANT_NOT_OPEN",
                        "message": (
                            "This restaurant is not currently accepting orders."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            subtotal = Decimal("0.00")

            for cart_item in cart_items:

                menu_item = cart_item.menu_item

                if not menu_item.is_available:
                    return Response(
                        {
                            "error": "MENU_ITEM_UNAVAILABLE",
                            "message": (
                                f"{menu_item.name} "
                                "is no longer available."
                            ),
                        },
                        status=status.HTTP_409_CONFLICT,
                    )

                subtotal += (
                    menu_item.price
                    * cart_item.quantity
                )

            order = Order.objects.create(
                customer=request.user,
                restaurant=cart.restaurant,
                subtotal=subtotal,
            )

            order_items = []

            for cart_item in cart_items:

                menu_item = cart_item.menu_item

                item_subtotal = (
                    menu_item.price
                    * cart_item.quantity
                )

                order_items.append(
                    OrderItem(
                        order=order,
                        menu_item=menu_item,
                        name_snapshot=menu_item.name,
                        unit_price=menu_item.price,
                        quantity=cart_item.quantity,
                        subtotal=item_subtotal,
                    )
                )

            OrderItem.objects.bulk_create(
                order_items
            )

            payment = Payment.objects.create(
            order=order,
            amount=subtotal,
            currency="INR",
            )

            cart.status = Cart.Status.CHECKED_OUT

            cart.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        order = (
            Order.objects
            .prefetch_related("items")
            .select_related("restaurant")
            .get(pk=order.pk)
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class RestaurantOrderListView(
    generics.ListAPIView
):

    serializer_class = OrderSerializer
    permission_classes = [
        IsRestaurantOwner
    ]

    def get_queryset(self):
        return (
            Order.objects
            .filter(
                restaurant__owner=self.request.user
            )
            .select_related(
                "restaurant",
                "customer",
            )
            .prefetch_related("items")
            .order_by("-created_at")
        )

class CustomerOrderListView(
    generics.ListAPIView
):

    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return (
            Order.objects
            .filter(
                customer=self.request.user
            )
            .select_related(
                "restaurant"
            )
            .prefetch_related("items")
            .order_by("-created_at")
        )

def get_restaurant_order(order_id, user):

    return (
        Order.objects
        .select_for_update()
        .select_related("restaurant")
        .filter(
            id=order_id,
            restaurant__owner=user,
        )
        .first()
    )

class AcceptOrderView(APIView):

    permission_classes = [
        IsRestaurantOwner
    ]

    def post(self, request, pk):

        with transaction.atomic():

            order = get_restaurant_order(
                pk,
                request.user,
            )

            if order is None:
                raise NotFound(
                    "Order not found."
                )

            if order.status != Order.Status.PENDING:
                return Response(
                    {
                        "error": "INVALID_ORDER_STATE",
                        "message": (
                            "Only pending orders "
                            "can be accepted."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )
            
            payment = order.payment

            if payment.status != PaymentStatus.SUCCESS:
                return Response(
                {
                    "code": "PAYMENT_REQUIRED",
                    "detail": "Order cannot be accepted until payment succeeds.",
                },
                status=status.HTTP_409_CONFLICT,
            )

            order.status = Order.Status.CONFIRMED

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return Response(
            OrderSerializer(order).data
        )

class RejectOrderView(APIView):

    permission_classes = [
        IsRestaurantOwner
    ]

    def post(self, request, pk):

        with transaction.atomic():

            order = get_restaurant_order(
                pk,
                request.user,
            )

            if order is None:
                raise NotFound(
                    "Order not found."
                )

            if order.status != Order.Status.PENDING:
                return Response(
                    {
                        "error": "INVALID_ORDER_STATE",
                        "message": (
                            "Only pending orders "
                            "can be rejected."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            order.status = Order.Status.REJECTED

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return Response(
            OrderSerializer(order).data
        )

class StartPreparingOrderView(APIView):

    permission_classes = [
        IsRestaurantOwner
    ]

    def post(self, request, pk):

        with transaction.atomic():

            order = get_restaurant_order(
                pk,
                request.user,
            )

            if order is None:
                raise NotFound(
                    "Order not found."
                )

            if order.status != Order.Status.CONFIRMED:
                return Response(
                    {
                        "error": "INVALID_ORDER_STATE",
                        "message": (
                            "Only confirmed orders "
                            "can enter preparation."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            order.status = Order.Status.PREPARING

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return Response(
            OrderSerializer(order).data
        )


class MarkOrderReadyView(APIView):

    permission_classes = [
        IsRestaurantOwner
    ]

    def post(self, request, pk):

        with transaction.atomic():

            order = get_restaurant_order(
                pk,
                request.user,
            )

            if order is None:
                raise NotFound(
                    "Order not found."
                )

            if order.status != Order.Status.PREPARING:
                return Response(
                    {
                        "error": "INVALID_ORDER_STATE",
                        "message": (
                            "Only preparing orders "
                            "can be marked ready."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            order.status = Order.Status.READY

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            OutboxEvent.objects.create(
                event_type="ORDER_READY",
                payload={
                    "order_id": order.id,
                },
            )

        return Response(
            OrderSerializer(order).data
        )