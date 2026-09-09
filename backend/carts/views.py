from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsCustomer

from .models import Cart, CartItem
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    UpdateCartItemSerializer,
    CartSerializer,
)


class AddCartItemView(APIView):
    permission_classes = [IsCustomer]


    def post(self, request):
        serializer = AddCartItemSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        menu_item = serializer.validated_data["menu_item"]
        quantity = serializer.validated_data["quantity"]

        restaurant = menu_item.category.restaurant

        if not menu_item.is_available:
            return Response(
                {
                    "error": "MENU_ITEM_UNAVAILABLE",
                    "message": "This menu item is currently unavailable.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        if restaurant.status != restaurant.Status.OPEN:
            return Response(
                {
                    "error": "RESTAURANT_NOT_OPEN",
                    "message": "This restaurant is not currently accepting orders.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        with transaction.atomic():

            cart = (
                Cart.objects
                .select_for_update()
                .filter(
                    customer=request.user,
                    status=Cart.Status.ACTIVE,
                )
                .first()
            )

            if cart is None:
                try:
                    cart = Cart.objects.create(
                        customer=request.user,
                        restaurant=restaurant,
                    )
                except IntegrityError:
                    cart = (
                        Cart.objects
                        .select_for_update()
                        .get(
                            customer=request.user,
                            status=Cart.Status.ACTIVE,
                        )
                    )

            if cart.restaurant_id != restaurant.id:
                return Response(
                    {
                        "error": "CART_RESTAURANT_MISMATCH",
                        "message": (
                            "Your cart contains items "
                            "from another restaurant."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            cart_item = (
                CartItem.objects
                .select_for_update()
                .filter(
                    cart=cart,
                    menu_item=menu_item,
                )
                .first()
            )

            if cart_item:
                cart_item.quantity += quantity
                cart_item.save(
                    update_fields=[
                        "quantity",
                        "updated_at",
                    ]
                )
            else:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    menu_item=menu_item,
                    quantity=quantity,
                )

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_200_OK,
        )


class CartView(APIView):

    permission_classes = [IsCustomer]

    def get(self, request):

        cart = (
            Cart.objects
            .prefetch_related(
                "items__menu_item"
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
                    "message": "Your cart is empty."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            CartSerializer(cart).data
        )

    def delete(self, request):

        with transaction.atomic():

            cart = (
                Cart.objects
                .select_for_update()
                .filter(
                    customer=request.user,
                    status=Cart.Status.ACTIVE,
                )
                .first()
            )

            if cart is None:
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )

            cart.items.all().delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class CartItemDetailView(APIView):

    permission_classes = [IsCustomer]

    def patch(self, request, pk):

        serializer = UpdateCartItemSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        with transaction.atomic():

            cart_item = (
                CartItem.objects
                .select_for_update()
                .select_related(
                    "cart",
                    "menu_item",
                )
                .filter(
                    id=pk,
                    cart__customer=request.user,
                    cart__status=Cart.Status.ACTIVE,
                )
                .first()
            )

            if cart_item is None:
                return Response(
                    {
                        "message": "Cart item not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not cart_item.menu_item.is_available:
                return Response(
                    {
                        "error": "MENU_ITEM_UNAVAILABLE",
                        "message": (
                            "This menu item is no longer available."
                        ),
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            cart_item.quantity = serializer.validated_data[
                "quantity"
            ]

            cart_item.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

        return Response(
            CartItemSerializer(cart_item).data
        )

        def delete(self, request, pk):

            with transaction.atomic():

                cart_item = (
                    CartItem.objects
                    .select_for_update()
                    .filter(
                        id=pk,
                        cart__customer=request.user,
                        cart__status=Cart.Status.ACTIVE,
                    )
                    .first()
                )

                if cart_item is None:
                    return Response(
                        {
                            "message": "Cart item not found."
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                cart_item.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )