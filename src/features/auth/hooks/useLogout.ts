// src/features/auth/hooks/useLogout.ts

import { useMutation } from "@tanstack/react-query";

import {
  queryClient,
  QUERY_KEYS,
} from "@/lib/react-query";

import { logout } from "../api";

export function useLogout() {
  return useMutation({
    mutationFn: logout,

    onSuccess: async () => {
      // Stop any active /me request
      await queryClient.cancelQueries({
        queryKey: QUERY_KEYS.auth.user,
      });

      // Mark current user as logged out
      queryClient.setQueryData(
        QUERY_KEYS.auth.user,
        null,
      );

      // Remove other authenticated cached data
      queryClient.removeQueries({
        predicate: (query) =>
          query.queryKey[0] !== "auth",
      });
    },
  });
}