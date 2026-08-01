// src/routes/AppRoutes.tsx

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import {
  AuthLayout,
  DashboardLayout,
} from "@/layouts";

import PublicRoute from "./guards/PublicRoute";
import ProtectedRoute from "./guards/ProtectedRoute";
import { ROUTES } from "@/routes/routeConfig";
import { LoginPage } from "@/features/auth/pages/LoginPage";
import { DashboardPage } from "@/features/dashboard/pages";
import NotFoundPage from "@/features/common/pages/NotFoundPage";

const router = createBrowserRouter([
  {
    element: <PublicRoute />,

    children: [
      {
        element: <AuthLayout />,

        children: [
          {
            path: ROUTES.LOGIN,
            element: <LoginPage />,
          },
        ],
      },
    ],
  },

  {
    element: <ProtectedRoute />,

    children: [
      {
        element: <DashboardLayout />,

        children: [
          {
            path: ROUTES.DASHBOARD,
            element: <DashboardPage />,
          },
        ],
      },
    ],
  },

  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default function AppRoutes() {
  return <RouterProvider router={router} />;
}