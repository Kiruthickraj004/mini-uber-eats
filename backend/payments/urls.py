from django.urls import path

from .views import PaymentDetailView, PaymentConfirmView


urlpatterns = [
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path(
        "<int:pk>/confirm/",
        PaymentConfirmView.as_view(),
        name="payment-confirm",
    ),
]