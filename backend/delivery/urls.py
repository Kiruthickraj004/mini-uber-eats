from django.urls import path

from .views import AvailableOrdersView, CompleteDeliveryView, DriverProfileView, ClaimDeliveryView, MyDeliveriesView, PickupDeliveryView


urlpatterns = [
    path("profile/", DriverProfileView.as_view()),
    path("orders/<int:order_id>/claim/", ClaimDeliveryView.as_view(), name="delivery-claim-order"),
    path("<int:delivery_id>/pickup/", PickupDeliveryView.as_view()),
    path("<int:delivery_id>/complete/",CompleteDeliveryView.as_view()),
    path("orders/available/",AvailableOrdersView.as_view()),
    path("my-deliveries/",MyDeliveriesView.as_view()),
]