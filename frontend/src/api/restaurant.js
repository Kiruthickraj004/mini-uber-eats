import request from "./client";

export function getRestaurants() {
  return request("/restaurants/");
}