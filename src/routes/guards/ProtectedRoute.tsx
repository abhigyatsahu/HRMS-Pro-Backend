import {
  Navigate,
  Outlet,
  useLocation,
} from "react-router-dom";

import { Loader2 } from "lucide-react";

import { ROUTES } from "@/routes/routeConfig";

import { useAuth } from "@/features/auth/hooks/useAuth";

export default function ProtectedRoute() {
  const location = useLocation();

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

  if (!isAuthenticated) {
    return (
      <Navigate
        to={ROUTES.LOGIN}
        replace
        state={{
          from: location,
        }}
      />
    );
  }

  return <Outlet />;
}