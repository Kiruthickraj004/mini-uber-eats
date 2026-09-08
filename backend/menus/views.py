from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.permissions import IsRestaurantOwner
from .serializers import MenuCategorySerializer, MenuItemSerializer
from .models import MenuCategory, MenuItem
from rest_framework.exceptions import PermissionDenied

class MenuCategoryCreateView(generics.CreateAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = [IsRestaurantOwner]

    def perform_create(self, serializer):
        restuarant = serializer.validated_data['restaurant']
        if self.request.user != restuarant.owner:
            raise PermissionDenied("You do not have permission to create a menu category for this restaurant.")
        serializer.save()


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsRestaurantOwner()]

        return [AllowAny()]

    def perform_create(self, serializer):
        category = serializer.validated_data['category']
        if self.request.user != category.restaurant.owner:
            raise PermissionDenied("You do not have permission to create a menu item for this category.")
        serializer.save()

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return MenuItem.objects.all()
        return MenuItem.objects.filter(category__restaurant__owner=self.request.user)

    def perform_update(self,serializer):
        serializer.save()