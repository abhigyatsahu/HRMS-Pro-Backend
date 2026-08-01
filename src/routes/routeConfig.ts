// src/routes/routeConfig.ts

export interface AppRoute {
  path: string;
  title: string;
  isPrivate: boolean;
}

export const ROUTES = {
  // Common
  ROOT: "/",

  // Authentication
  LOGIN: "/login",
  FORGOT_PASSWORD: "/forgot-password",
  RESET_PASSWORD: "/reset-password",

  // Dashboard
  DASHBOARD: "/dashboard",

  // Organization
  ORGANIZATION: "/organization",

  // Employee Management
  EMPLOYEES: "/employees",
  DEPARTMENTS: "/departments",
  DESIGNATIONS: "/designations",

  // Attendance & Leave
  ATTENDANCE: "/attendance",
  LEAVES: "/leaves",
  HOLIDAYS: "/holidays",

  // Payroll
  PAYROLL: "/payroll",

  // Documents
  DOCUMENTS: "/documents",

  // Reports
  REPORTS: "/reports",

  // User
  PROFILE: "/profile",
  NOTIFICATIONS: "/notifications",
  SETTINGS: "/settings",

  // Error Pages
  UNAUTHORIZED: "/403",
  SERVER_ERROR: "/500",
  NOT_FOUND: "*",
} as const;