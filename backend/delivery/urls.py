from django.urls import path

from .views import CompleteDeliveryView, DriverProfileView, ClaimDeliveryView, PickupDeliveryView


urlpatterns = [
    path("profile/", DriverProfileView.as_view()),
    path("orders/<int:order_id>/claim/",ClaimDeliveryView.as_view()),
    path("<int:delivery_id>/pickup/", PickupDeliveryView.as_view()),
    path("<int:delivery_id>/complete/",CompleteDeliveryView.as_view()),
]