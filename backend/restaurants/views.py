from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.permissions import IsRestaurantOwner

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):

        if self.request.method == "POST":
            return [IsRestaurantOwner()]

        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = RestaurantSerializer

    permission_classes = [
        IsRestaurantOwner
    ]

    def get_queryset(self):
        return Restaurant.objects.filter(
            owner=self.request.user
        )