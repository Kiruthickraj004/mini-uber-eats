import request from "./client";

export function getPayment(paymentId) {
  return request(`/payments/${paymentId}/`);
}

export function confirmPayment(paymentId, idempotencyKey) {
  return request(`/payments/${paymentId}/confirm/`, {
    method: "POST",
    headers: {
      "Idempotency-Key": idempotencyKey,
    },
  });
}