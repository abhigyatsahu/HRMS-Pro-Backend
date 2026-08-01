// src/features/auth/pages/LoginPage.tsx

import { LoginForm } from "../components";

export function LoginPage() {
  return (
    <div className="w-full max-w-md">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight">
          Welcome back
        </h1>

        <p className="mt-2 text-sm text-muted-foreground">
          Sign in to continue to HRMS Pro.
        </p>
      </div>

      <LoginForm />
    </div>
  );
}