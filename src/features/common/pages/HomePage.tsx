// src/features/common/pages/HomePage.tsx

import { Navigate } from "react-router-dom";
import { ROUTES } from "@/routes";

export default function HomePage() {
  return <Navigate to={ROUTES.LOGIN} replace />;
}