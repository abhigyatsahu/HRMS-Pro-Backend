// src/services/storage.service.ts

export const storageService = {
  get<T>(key: string): T | null {
    const value = localStorage.getItem(key);

    if (!value) return null;

    return JSON.parse(value) as T;
  },

  set(key: string, value: unknown) {
    localStorage.setItem(
      key,
      JSON.stringify(value)
    );
  },

  remove(key: string) {
    localStorage.removeItem(key);
  },

  clear() {
    localStorage.clear();
  },
};