// src/features/common/routes.tsx

import HomePage from "./pages/HomePage";
import NotFoundPage from "./pages/NotFoundPage";

import { ROUTES } from "@/routes";

export const commonRoutes = [
  {
    path: ROUTES.ROOT,
    element: <HomePage />,
  },
  {
    path: ROUTES.NOT_FOUND,
    element: <NotFoundPage />,
  },
];