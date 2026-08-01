// src/routes/guards/PublicRoute.tsx

import {
  Navigate,
  Outlet,
} from "react-router-dom";

import { Loader2 } from "lucide-react";

import { ROUTES } from "@/routes/routeConfig";

import { useAuth } from "@/features/auth/hooks/useAuth";

export default function PublicRoute() {
  const {
    isAuthenticated,
    isLoading,
  } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="size-7 animate-spin text-primary" />
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <Navigate
        to={ROUTES.DASHBOARD}
        replace
      />
    );
  }

  return <Outlet />;
}