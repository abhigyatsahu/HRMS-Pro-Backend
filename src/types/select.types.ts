// src/types/select.types.ts

export interface SelectOption<T = string> {
  label: string;
  value: T;
  disabled?: boolean;
}