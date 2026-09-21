import request from "./client";

export function getCart() {
  return request("/cart/");
}

export function addToCart(menuItemId, quantity = 1) {
  return request("/cart/items/", {
    method: "POST",
    body: JSON.stringify({
      menu_item: menuItemId,
      quantity,
    }),
  });
}

export function updateCartItem(itemId, quantity) {
  return request(`/cart/items/${itemId}/`, {
    method: "PATCH",
    body: JSON.stringify({
      quantity,
    }),
  });
}

export function removeCartItem(itemId) {
  return request(`/cart/items/${itemId}/`, {
    method: "DELETE",
  });
}

export function clearCart() {
  return request("/cart/", {
    method: "DELETE",
  });
}