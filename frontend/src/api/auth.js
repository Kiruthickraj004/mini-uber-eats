import request from "./client";

export function registerUser(data) {
  return request("/users/register/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function login(username, password) {
  return request("/auth/token/", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
    }),
  });
}


export function refreshAccessToken(refresh) {
  return request("/auth/token/refresh/", {
    method: "POST",
    body: JSON.stringify({
      refresh,
    }),
  });
}

export function getMe() {
  return request("/users/me/");
}