// src/layouts/ErrorLayout.tsx

import { Outlet } from "react-router-dom";

export default function ErrorLayout() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <Outlet />
    </div>
  );
}