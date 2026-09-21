import request from "./client";

export function getRestaurantMenu(restaurantId) {
  return request(
    `/menu/items/?restaurant=${restaurantId}`
  );
}