from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from config.rate_limit import is_rate_limited
from .models import Payment,PaymentAttempt,PaymentStatus
from .serializers import PaymentSerializer

class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        payment = get_object_or_404(
            Payment.objects.select_related("order"),
            pk=pk,
            order__customer=request.user,
        )

        return Response(
            PaymentSerializer(payment).data
        )

class PaymentConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        idempotency_key = request.headers.get("Idempotency-Key")

        if not idempotency_key:
            return Response(
                {
                    "code": "IDEMPOTENCY_KEY_REQUIRED",
                    "detail": "Idempotency-Key header is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # First verify that this payment belongs to the authenticated user.
        payment = (
            Payment.objects
            .select_related("order")
            .filter(
                pk=pk,
                order__customer=request.user,
            )
            .first()
        )

        if payment is None:
            return Response(
                {
                    "code": "PAYMENT_NOT_FOUND",
                    "detail": "Payment not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Rate limit this specific customer's confirmation attempts
        # for this specific payment.
        key = f"rate:payment-confirm:{request.user.id}:{payment.id}"

        if is_rate_limited(
            key=key,
            limit=5,
            window=60,
        ):
            return Response(
                {
                    "code": "RATE_LIMITED",
                    "detail": "Too many payment confirmation attempts. Try again later.",
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        try:
            with transaction.atomic():
                payment = (
                    Payment.objects
                    .select_for_update()
                    .select_related("order")
                    .filter(
                        pk=pk,
                        order__customer=request.user,
                    )
                    .first()
                )

                if payment is None:
                    return Response(
                        {
                            "code": "PAYMENT_NOT_FOUND",
                            "detail": "Payment not found.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Retry with the same idempotency key
                existing_attempt = (
                    PaymentAttempt.objects
                    .filter(idempotency_key=idempotency_key)
                    .first()
                )

                if existing_attempt:
                    return Response(
                        {
                            "payment_id": payment.id,
                            "status": existing_attempt.status,
                            "provider_reference": (
                                existing_attempt.provider_reference
                            ),
                        }
                    )

                # Payment already completed using another request
                if payment.status == PaymentStatus.SUCCESS:
                    return Response(
                        {
                            "payment_id": payment.id,
                            "status": payment.status,
                            "detail": "Payment has already been completed.",
                        }
                    )

                # Simulate successful provider confirmation
                payment.status = PaymentStatus.SUCCESS
                payment.save(update_fields=["status", "updated_at"])

                attempt = PaymentAttempt.objects.create(
                    payment=payment,
                    idempotency_key=idempotency_key,
                    status=PaymentStatus.SUCCESS,
                    provider_reference=f"SIM-{payment.id}-{idempotency_key[:8]}",
                )

                return Response(
                    {
                        "payment_id": payment.id,
                        "status": payment.status,
                        "provider_reference": attempt.provider_reference,
                    }
                )

        except IntegrityError:
            existing_attempt = PaymentAttempt.objects.get(
                idempotency_key=idempotency_key
            )

            return Response(
                {
                    "payment_id": existing_attempt.payment_id,
                    "status": existing_attempt.status,
                    "provider_reference": existing_attempt.provider_reference,
                }
            )