// src/features/auth/hooks/useLogin.ts

import { useMutation } from "@tanstack/react-query";

import {
  queryClient,
  QUERY_KEYS,
} from "@/lib/react-query";

import {
  getCurrentUser,
  initializeCsrf,
  login,
} from "../api";

import type { LoginCredentials } from "../types";

export function useLogin() {
  return useMutation({
    mutationFn: async (
      credentials: LoginCredentials,
    ) => {
      await initializeCsrf();

      await login(credentials);

      return getCurrentUser();
    },

    onSuccess: (user) => {
      queryClient.setQueryData(
        QUERY_KEYS.auth.user,
        user,
      );
    },
  });
}