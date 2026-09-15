from django.core.cache import cache
from django.db import transaction

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.permissions import IsRestaurantOwner

from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer
from .cache import (
    restaurant_menu_cache_key,
    invalidate_restaurant_menu,
)


class MenuCategoryCreateView(generics.CreateAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = [IsRestaurantOwner]

    def perform_create(self, serializer):
        restaurant = serializer.validated_data["restaurant"]

        if self.request.user != restaurant.owner:
            raise PermissionDenied(
                "You do not have permission to create a menu category "
                "for this restaurant."
            )

        serializer.save()


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsRestaurantOwner()]

        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        restaurant_id = self.kwargs.get("restaurant_id")

        if restaurant_id is None:
            restaurant_id = request.query_params.get("restaurant_id")

        # No restaurant filter → use normal DRF behavior
        if restaurant_id is None:
            return super().list(request, *args, **kwargs)

        cache_key = restaurant_menu_cache_key(restaurant_id)

        # -------------------------
        # Cache HIT
        # -------------------------
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        # -------------------------
        # Cache MISS
        # -------------------------
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                category__restaurant_id=restaurant_id
            )
        )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        # Store serialized response in Redis
        cache.set(
            cache_key,
            serializer.data,
            timeout=300,
        )

        return Response(serializer.data)

    def perform_create(self, serializer):
        category = serializer.validated_data["category"]

        if self.request.user != category.restaurant.owner:
            raise PermissionDenied(
                "You do not have permission to create a menu item "
                "for this category."
            )

        menu_item = serializer.save()

        restaurant_id = menu_item.category.restaurant_id

        # Invalidate cache only after DB transaction commits
        transaction.on_commit(
            lambda: invalidate_restaurant_menu(restaurant_id)
        )


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return MenuItem.objects.all()

        return MenuItem.objects.filter(
            category__restaurant__owner=self.request.user
        )

    def perform_update(self, serializer):
        menu_item = serializer.save()

        restaurant_id = menu_item.category.restaurant_id

        # Invalidate cache after successful DB commit
        transaction.on_commit(
            lambda: invalidate_restaurant_menu(restaurant_id)
        )

    def perform_destroy(self, instance):
        restaurant_id = instance.category.restaurant_id

        instance.delete()

        # Invalidate cache after successful DB commit
        transaction.on_commit(
            lambda: invalidate_restaurant_menu(restaurant_id)
        )