// src/constants/roles.constants.ts

export const ROLES = {
  SUPER_ADMIN: "SUPER_ADMIN",
  ADMIN: "ADMIN",
  HR_MANAGER: "HR_MANAGER",
  MANAGER: "MANAGER",
  EMPLOYEE: "EMPLOYEE",
} as const;

export type Role =
  (typeof ROLES)[keyof typeof ROLES];