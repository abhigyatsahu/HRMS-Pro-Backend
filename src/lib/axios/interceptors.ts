import type {
  AxiosError,
  InternalAxiosRequestConfig,
} from "axios";

import { API_ENDPOINTS } from "@/api/endpoints";

import { apiClient } from "./client";


interface RetryRequestConfig
  extends InternalAxiosRequestConfig {
  _retry?: boolean;
}


let refreshPromise: Promise<unknown> | null = null;


apiClient.interceptors.response.use(
  (response) => response,

  async (error: AxiosError) => {
    const originalRequest =
      error.config as RetryRequestConfig | undefined;

    if (
      error.response?.status !== 401 ||
      !originalRequest
    ) {
      return Promise.reject(error);
    }

    const url = originalRequest.url ?? "";

    const isAuthRequest =
      url.includes(API_ENDPOINTS.AUTH.LOGIN) ||
      url.includes(API_ENDPOINTS.AUTH.LOGOUT) ||
      url.includes(API_ENDPOINTS.AUTH.REFRESH);

    if (
      originalRequest._retry ||
      isAuthRequest
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      if (!refreshPromise) {
        refreshPromise = apiClient.post(
          API_ENDPOINTS.AUTH.REFRESH,
        );
      }

      await refreshPromise;

      return apiClient(originalRequest);
    } catch (refreshError) {
      return Promise.reject(refreshError);
    } finally {
      refreshPromise = null;
    }
  },
);