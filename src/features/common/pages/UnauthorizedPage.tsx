// src/features/common/pages/UnauthorizedPage.tsx

import { Link } from "react-router-dom";

import { ROUTES } from "@/routes";

export default function UnauthorizedPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-6xl font-bold">403</h1>

      <p className="text-muted-foreground">
        You don't have permission to access this page.
      </p>

      <Link
        to={ROUTES.ROOT}
        className="rounded-md bg-primary px-4 py-2 text-primary-foreground"
      >
        Back to Home
      </Link>
    </div>
  );
}