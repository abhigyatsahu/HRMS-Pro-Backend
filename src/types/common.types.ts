// src/types/common.types.ts

export type ID = string;

export type UUID = string;

export type SortDirection = "asc" | "desc";

export type Status =
  | "active"
  | "inactive";

export interface TimestampFields {
  createdAt: string;
  updatedAt: string;
}

export interface BaseEntity extends TimestampFields {
  id: ID;
  uuid: UUID;
}

export interface SortParams {
  sortBy?: string;
  sortDirection?: SortDirection;
}

export interface SearchParams {
  search?: string;
}