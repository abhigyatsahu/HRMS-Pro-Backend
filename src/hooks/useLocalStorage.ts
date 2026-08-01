// src/hooks/useLocalStorage.ts

import { useState } from "react";

import { storageService } from "@/services";

export function useLocalStorage<T>(
  key: string,
  initialValue: T
) {
  const [value, setValue] = useState<T>(() => {
    return storageService.get<T>(key) ?? initialValue;
  });

  const setStoredValue = (newValue: T) => {
    setValue(newValue);
    storageService.set(key, newValue);
  };

  return [value, setStoredValue] as const;
}