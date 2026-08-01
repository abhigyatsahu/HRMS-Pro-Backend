// src/config/theme.ts

export const THEME = {
  DEFAULT: "light",

  STORAGE_KEY: "theme",

  THEMES: {
    LIGHT: "light",
    DARK: "dark",
    SYSTEM: "system",
  },
} as const;

export type Theme = (typeof THEME.THEMES)[keyof typeof THEME.THEMES];