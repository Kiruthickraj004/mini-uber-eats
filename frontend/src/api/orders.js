import request from "./client";

export function checkout() {
  return request("/orders/checkout/", {
    method: "POST",
  });
}

export function getOrders() {
  return request("/orders/");
}

export function getOrder(orderId) {
  return request(`/orders/${orderId}/`);
}

export function getRestaurantOrders() {
  return request("/orders/restaurant/");
}

export function acceptOrder(orderId) {
  return request(`/orders/${orderId}/accept/`, {
    method: "POST",
  });
}

export function rejectOrder(orderId) {
  return request(`/orders/${orderId}/reject/`, {
    method: "POST",
  });
}

export function startPreparing(orderId) {
  return request(
    `/orders/${orderId}/start-preparing/`,
    {
      method: "POST",
    }
  );
}

export function markOrderReady(orderId) {
  return request(`/orders/${orderId}/ready/`, {
    method: "POST",
  });
}