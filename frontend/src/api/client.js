const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL;

import {
  getAccessToken,
  getRefreshToken,
  saveTokens,
  clearTokens,
} from "./authStorage";

let refreshPromise = null;

async function refreshAccessToken() {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    clearTokens();
    throw new Error("Your session has expired. Please log in again.");
  }

  const response = await fetch(
    `${API_BASE_URL}/auth/token/refresh/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    }
  );

  if (!response.ok) {
    clearTokens();

    throw new Error(
      "Your session has expired. Please log in again."
    );
  }

  const data = await response.json();

  saveTokens(
    data.access,
    data.refresh ?? refreshToken
  );

  return data.access;
}

async function request(
  path,
  options = {},
  retry = true
) {
  const token = getAccessToken();

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {}),
        ...(options.headers || {}),
      },
    }
  );

  const isAuthEndpoint = path.startsWith("/auth/");

  if (
    response.status === 401 &&
    retry &&
    !isAuthEndpoint
  ) {
    if (!refreshPromise) {
      refreshPromise = refreshAccessToken()
        .finally(() => {
          refreshPromise = null;
        });
    }

    try {
      await refreshPromise;

      return request(
        path,
        options,
        false
      );
    } catch (error) {
      throw error;
    }
  }

  const responseText = await response.text();
  let data = {};

  if (responseText) {
    try {
      data = JSON.parse(responseText);
    } catch {
      data = {
        detail:
          "The server returned an unexpected response.",
      };
    }
  }

  if (!response.ok) {
    const message =
      data.detail ||
      data.message ||
      data.error ||
      data.non_field_errors?.[0] ||
      "Something went wrong";

    throw new Error(message);
  }

  return data;
}

export default request;