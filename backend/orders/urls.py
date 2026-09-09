from django.urls import path

from .views import (
    AcceptOrderView,
    CheckoutView,
    CustomerOrderListView,
    MarkOrderReadyView,
    RejectOrderView,
    RestaurantOrderListView,
    StartPreparingOrderView,
)


urlpatterns = [
    path(
        "checkout/",
        CheckoutView.as_view(),
        name="checkout",
    ),

    path(
        "",
        CustomerOrderListView.as_view(),
        name="customer-orders",
    ),

    path(
        "restaurant/",
        RestaurantOrderListView.as_view(),
        name="restaurant-orders",
    ),

    path(
        "<int:pk>/accept/",
        AcceptOrderView.as_view(),
        name="order-accept",
    ),

    path(
        "<int:pk>/reject/",
        RejectOrderView.as_view(),
        name="order-reject",
    ),

    path(
        "<int:pk>/start-preparing/",
        StartPreparingOrderView.as_view(),
        name="order-start-preparing",
    ),

    path(
        "<int:pk>/ready/",
        MarkOrderReadyView.as_view(),
        name="order-ready",
    ),
]