// src/layouts/AuthLayout.tsx

import { Outlet } from "react-router-dom";

import {
  Building2,
} from "lucide-react";

export default function AuthLayout() {
  return (
    <main className="grid min-h-screen lg:grid-cols-2">
      <section
        className="
          hidden
          bg-primary
          p-12
          text-primary-foreground
          lg:flex
          lg:flex-col
          lg:justify-between
        "
      >
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-white/10 p-2">
            <Building2 className="size-6" />
          </div>

          <span className="text-xl font-semibold">
            HRMS Pro
          </span>
        </div>

        <div className="max-w-lg">
          <h2 className="text-4xl font-semibold leading-tight">
            Manage your people.
            <br />
            Empower your organization.
          </h2>

          <p className="mt-5 text-primary-foreground/80">
            Employees, attendance, leave,
            payroll and workforce insights
            from one secure workspace.
          </p>
        </div>

        <p className="text-sm text-primary-foreground/60">
          © {new Date().getFullYear()} HRMS Pro
        </p>
      </section>

      <section
        className="
          flex
          items-center
          justify-center
          bg-background
          px-6
          py-12
        "
      >
        <Outlet />
      </section>
    </main>
  );
}