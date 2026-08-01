// src/layouts/dashboard/DashboardHeader.tsx

import { LogOut } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ROUTES } from "@/routes/routeConfig";
import { useLogout } from "@/features/auth/hooks/useLogout";

export default function DashboardHeader() {
  const logoutMutation = useLogout();
  const navigate = useNavigate();

  const handleLogout = async () => {
  try {
    await logoutMutation.mutateAsync();

    navigate(
      ROUTES.LOGIN,
      {
        replace: true,
      },
    );
  } catch (error) {
    console.error(
      "Logout failed:",
      error,
    );
  }
};

  return (
    <header className="flex h-16 items-center justify-between border-b bg-background px-6">
      <div>
        <h2 className="font-semibold">
          HRMS Pro
        </h2>
      </div>

      <Button
        variant="outline"
        onClick={handleLogout}
        disabled={logoutMutation.isPending}
      >
        <LogOut />

        {logoutMutation.isPending
          ? "Logging out..."
          : "Logout"}
      </Button>
    </header>
  );
}
