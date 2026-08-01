// src/api/errors.ts

import axios from "axios";

interface ApiErrorResponse {
  detail?: string;
  message?: string;

  non_field_errors?: string[];

  [key: string]:
    | string
    | string[]
    | undefined;
}

export function getApiErrorMessage(
  error: unknown,
): string {
  if (axios.isAxiosError<ApiErrorResponse>(error)) {
    const data = error.response?.data;

    if (data?.message) {
      return data.message;
    }

    if (data?.detail) {
      return data.detail;
    }

    if (data?.non_field_errors?.length) {
      return data.non_field_errors[0];
    }

    return "Unable to complete the request.";
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong.";
}