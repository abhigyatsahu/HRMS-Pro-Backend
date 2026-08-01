// src/constants/regex.constants.ts

export const REGEX = {
  EMAIL:
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/,

  PHONE:
    /^[0-9]{10,15}$/,

  INDIAN_PHONE:
    /^[6-9]\d{9}$/,

  PIN_CODE:
    /^[1-9][0-9]{5}$/,

  ALPHANUMERIC:
    /^[a-zA-Z0-9]+$/,

  ALPHABETS_ONLY:
    /^[a-zA-Z\s]+$/,

  STRONG_PASSWORD:
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/,
} as const;