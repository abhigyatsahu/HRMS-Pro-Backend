// src/config/env.ts

export const ENV = {
  API_URL: import.meta.env.VITE_API_URL,

  APP_NAME: import.meta.env.VITE_APP_NAME,

  MODE: import.meta.env.MODE,

  DEV: import.meta.env.DEV,

  PROD: import.meta.env.PROD,
} as const;