// src/features/auth/api/auth.api.ts

import { API_ENDPOINTS } from "@/api/endpoints";
import { apiClient } from "@/lib/axios";

import type {
  CsrfResponse,
  CurrentUserResponse,
  LoginCredentials,
  LoginResponse,
} from "../types";


export async function initializeCsrf() {
  const response =
    await apiClient.get<CsrfResponse>(
      API_ENDPOINTS.AUTH.CSRF,
    );

  return response.data;
}


export async function login(
  credentials: LoginCredentials,
) {
  const response =
    await apiClient.post<LoginResponse>(
      API_ENDPOINTS.AUTH.LOGIN,
      credentials,
    );

  return response.data;
}


export async function logout() {
  const response =
    await apiClient.post<LoginResponse>(
      API_ENDPOINTS.AUTH.LOGOUT,
      {},
    );

  return response.data;
}


export async function getCurrentUser() {
  const response =
    await apiClient.get<CurrentUserResponse>(
      API_ENDPOINTS.AUTH.ME,
    );

  return response.data.data;
}


export async function refreshSession() {
  const response =
    await apiClient.post<LoginResponse>(
      API_ENDPOINTS.AUTH.REFRESH,
    );

  return response.data;
}