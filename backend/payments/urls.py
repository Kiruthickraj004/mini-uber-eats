from django.urls import path

from .views import PaymentDetailView, PaymentConfirmView


urlpatterns = [
    path("<int:pk>/", PaymentDetailView.as_view()),
    path(
        "<int:pk>/confirm/",
        PaymentConfirmView.as_view(),
    ),
]