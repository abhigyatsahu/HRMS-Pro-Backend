// src/config/navigation/breadcrumbs.ts

export interface BreadcrumbItem {
  path: string;
  label: string;
}

export const BREADCRUMBS: BreadcrumbItem[] = [
  {
    path: "/dashboard",
    label: "Dashboard",
  },
  {
    path: "/employees",
    label: "Employees",
  },
  {
    path: "/employees/create",
    label: "Create Employee",
  },
  {
    path: "/attendance",
    label: "Attendance",
  },
  {
    path: "/leaves",
    label: "Leaves",
  },
  {
    path: "/reports",
    label: "Reports",
  },
  {
    path: "/settings",
    label: "Settings",
  },
];