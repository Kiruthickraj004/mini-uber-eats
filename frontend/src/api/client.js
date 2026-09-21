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
    throw new Error("No refresh token available");
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
      "Session expired. Please login again."
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

  if (
    response.status === 401 &&
    retry
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

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Something went wrong"
    );
  }

  return data;
}

export default request;