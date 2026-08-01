// src/api/endpoints.ts

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: "/auth/login/",
    LOGOUT: "/auth/logout/",
    REFRESH: "/auth/refresh/",
    CSRF: "/auth/csrf/",
    ME:"/auth/me/"
  },

  DASHBOARD: {
    STATS: "/dashboard/stats/",
  },

  EMPLOYEES: {
    LIST: "/employees/",
    CREATE: "/employees/",
    DETAILS: (id: string) => `/employees/${id}/`,
    UPDATE: (id: string) => `/employees/${id}/`,
    DELETE: (id: string) => `/employees/${id}/`,
  },

  DEPARTMENTS: {
    LIST: "/departments/",
    CREATE: "/departments/",
    DETAILS: (id: string) => `/departments/${id}/`,
    UPDATE: (id: string) => `/departments/${id}/`,
    DELETE: (id: string) => `/departments/${id}/`,
  },

  ATTENDANCE: {
    LIST: "/attendance/",
  },

  LEAVES: {
    LIST: "/leaves/",
  },

  REPORTS: {
    LIST: "/reports/",
  },
} as const;