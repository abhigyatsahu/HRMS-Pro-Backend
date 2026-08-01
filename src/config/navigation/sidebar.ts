// src/config/navigation/sidebar.ts

import type { LucideIcon } from "lucide-react";

export interface SidebarItem {
  title: string;
  path: string;
  icon?: LucideIcon;
  permissions?: string[];
  children?: SidebarItem[];
}

export const SIDEBAR_NAVIGATION: SidebarItem[] = [
  {
    title: "Dashboard",
    path: "/dashboard",
  },
  {
    title: "Organization",
    path: "/organization",
  },
  {
    title: "Employees",
    path: "/employees",
  },
  {
    title: "Departments",
    path: "/departments",
  },
  {
    title: "Designations",
    path: "/designations",
  },
  {
    title: "Attendance",
    path: "/attendance",
  },
  {
    title: "Leaves",
    path: "/leaves",
  },
  {
    title: "Holidays",
    path: "/holidays",
  },
  {
    title: "Payroll",
    path: "/payroll",
  },
  {
    title: "Documents",
    path: "/documents",
  },
  {
    title: "Reports",
    path: "/reports",
  },
  {
    title: "Notifications",
    path: "/notifications",
  },
  {
    title: "Settings",
    path: "/settings",
  },
];