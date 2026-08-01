// src/features/common/pages/NotFoundPage.tsx

import { Link } from "react-router-dom";

import { ROUTES } from "@/routes";

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background px-4">
      <h1 className="text-7xl font-bold">404</h1>

      <p className="text-muted-foreground text-lg">
        The page you are looking for doesn't exist.
      </p>

      <Link
        to={ROUTES.ROOT}
        className="rounded-md bg-primary px-4 py-2 text-primary-foreground"
      >
        Go Home
      </Link>
    </div>
  );
}