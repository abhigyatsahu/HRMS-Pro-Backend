// src/constants/permissions.constants.ts

export const PERMISSIONS = {
  EMPLOYEE: {
    VIEW: "employee.view",
    CREATE: "employee.create",
    UPDATE: "employee.update",
    DELETE: "employee.delete",
  },

  DEPARTMENT: {
    VIEW: "department.view",
    CREATE: "department.create",
    UPDATE: "department.update",
    DELETE: "department.delete",
  },

  ATTENDANCE: {
    VIEW: "attendance.view",
    CREATE: "attendance.create",
    UPDATE: "attendance.update",
    DELETE: "attendance.delete",
  },

  LEAVE: {
    VIEW: "leave.view",
    CREATE: "leave.create",
    APPROVE: "leave.approve",
    REJECT: "leave.reject",
    DELETE: "leave.delete",
  },

  PAYROLL: {
    VIEW: "payroll.view",
    CREATE: "payroll.create",
    UPDATE: "payroll.update",
    PROCESS: "payroll.process",
  },

  REPORT: {
    VIEW: "report.view",
    EXPORT: "report.export",
  },

  SETTINGS: {
    VIEW: "settings.view",
    UPDATE: "settings.update",
  },
} as const;