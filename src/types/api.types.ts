// src/types/api.types.ts

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export interface ApiError {
  message: string;
  detail?: string;
  code?: string;
  errors?: Record<string, string[]>;
}

export type ApiStatus =
  | "idle"
  | "loading"
  | "success"
  | "error";