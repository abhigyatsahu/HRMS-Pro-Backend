// src/config/app.ts

export const APP_CONFIG = {
  NAME: import.meta.env.VITE_APP_NAME,
  VERSION: "1.0.0",

  PAGINATION: {
    DEFAULT_PAGE: 1,
    DEFAULT_PAGE_SIZE: 10,
    PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  },

  DATE_FORMAT: "DD MMM YYYY",

  DATETIME_FORMAT: "DD MMM YYYY hh:mm A",

  STORAGE_KEYS: {
    ACCESS_TOKEN: "accessToken",
    REFRESH_TOKEN: "refreshToken",
    USER: "user",
    THEME: "theme",
  },
} as const;