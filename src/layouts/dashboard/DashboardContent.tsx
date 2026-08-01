// src/layouts/dashboard/DashboardContent.tsx

import { Outlet } from "react-router-dom";

export default function DashboardContent() {
  return (
    <main className="flex-1 overflow-auto p-6">
      <Outlet />
    </main>
  );
}