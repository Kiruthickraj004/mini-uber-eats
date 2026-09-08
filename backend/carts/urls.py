from django.urls import path

from .views import AddCartItemView


urlpatterns = [
    path(
        "items/",
        AddCartItemView.as_view(),
        name="cart-item-add",
    ),
]