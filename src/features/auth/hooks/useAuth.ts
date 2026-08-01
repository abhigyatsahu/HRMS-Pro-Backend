// src/features/auth/hooks/useAuth.ts

import { useQuery } from "@tanstack/react-query";

import { QUERY_KEYS } from "@/lib/react-query";

import { getCurrentUser } from "../api";

import type { AuthUser } from "../types";

export function useAuth() {
  const query = useQuery<
    AuthUser | null
  >({
    queryKey: QUERY_KEYS.auth.user,

    queryFn: getCurrentUser,

    retry: false,

    staleTime: 5 * 60 * 1000,

    refetchInterval: false,

    refetchOnWindowFocus: false,

    refetchOnReconnect: true,
  });

  return {
    user: query.data ?? null,

    isAuthenticated:
      query.data != null,

    isLoading: query.isPending,

    isError: query.isError,

    error: query.error,

    refetch: query.refetch,
  };
}