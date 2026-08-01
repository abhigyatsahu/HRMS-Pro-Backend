// src/types/pagination.types.ts

export interface PaginationParams {
  page?: number;
  pageSize?: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PaginationState {
  page: number;
  pageSize: number;
  totalItems: number;
}