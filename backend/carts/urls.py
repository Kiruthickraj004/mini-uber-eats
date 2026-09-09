from django.urls import path

from .views import (
    AddCartItemView,
    CartView,
    CartItemDetailView,
)


urlpatterns = [
    path(
        "",
        CartView.as_view(),
        name="cart",
    ),

    path(
        "items/",
        AddCartItemView.as_view(),
        name="cart-item-add",
    ),

    path(
    "items/<int:pk>/",
        CartItemDetailView.as_view(),
        name="cart-item-detail",
    ),
]