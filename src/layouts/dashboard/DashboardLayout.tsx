// src/layouts/dashboard/DashboardLayout.tsx

import DashboardContent from "./DashboardContent";
import DashboardFooter from "./DashboardFooter";
import DashboardHeader from "./DashboardHeader";
import DashboardSidebar from "./DashboardSidebar";

export default function DashboardLayout() {
  return (
    <div className="flex min-h-screen bg-background">
      <DashboardSidebar />

      <div className="flex flex-1 flex-col">
        <DashboardHeader />

        <DashboardContent />

        <DashboardFooter />
      </div>
    </div>
  );
}