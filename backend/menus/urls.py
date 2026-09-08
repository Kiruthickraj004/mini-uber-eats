from django.urls import path

from .views import (
    MenuCategoryCreateView,
    MenuItemDetailView,
    MenuItemListCreateView,
)


urlpatterns = [
    path(
        "categories/",
        MenuCategoryCreateView.as_view(),
        name="category-create",
    ),

    path(
        "items/",
        MenuItemListCreateView.as_view(),
        name="item-list-create",
    ),

    path(
        "items/<int:pk>/",
        MenuItemDetailView.as_view(),
        name="item-detail",
    ),
]