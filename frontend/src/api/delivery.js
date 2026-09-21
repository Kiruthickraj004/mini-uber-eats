import request from "./client";

export function createDriverProfile(data) {
  return request("/delivery/profile/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getDriverProfile() {
  return request("/delivery/profile/");
}

export function updateDriverProfile(data) {
  return request("/delivery/profile/", {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function claimOrder(orderId) {
  return request(
    `/delivery/orders/${orderId}/claim/`,
    {
      method: "POST",
    }
  );
}

export function pickupDelivery(deliveryId) {
  return request(
    `/delivery/${deliveryId}/pickup/`,
    {
      method: "POST",
    }
  );
}

export function completeDelivery(deliveryId) {
  return request(
    `/delivery/${deliveryId}/complete/`,
    {
      method: "POST",
    }
  );
}

export function getAvailableOrders() {
  return request("/delivery/orders/available/");
}

export function getMyDeliveries() {
  return request("/delivery/my-deliveries/");
}