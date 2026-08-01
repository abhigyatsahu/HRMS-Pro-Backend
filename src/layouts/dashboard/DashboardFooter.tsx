// src/layouts/dashboard/DashboardFooter.tsx

export default function DashboardFooter() {
  return (
    <footer className="border-t px-6 py-4 text-center text-sm text-muted-foreground">
      © {new Date().getFullYear()} HRMS Pro. All rights reserved.
    </footer>
  );
}