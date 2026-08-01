// src/features/common/pages/ServerErrorPage.tsx

import { Link } from "react-router-dom";

import { ROUTES } from "@/routes";

export default function ServerErrorPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-6xl font-bold">500</h1>

      <p className="text-muted-foreground">
        Something went wrong.
      </p>

      <Link
        to={ROUTES.ROOT}
        className="rounded-md bg-primary px-4 py-2 text-primary-foreground"
      >
        Try Again
      </Link>
    </div>
  );
}