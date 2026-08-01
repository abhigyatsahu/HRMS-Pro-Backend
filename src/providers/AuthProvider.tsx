// src/providers/AuthProvider.tsx

import { createContext } from "react";
import type { PropsWithChildren } from "react";

interface AuthContextValue {
  isAuthenticated: boolean;
}

export const AuthContext =
  createContext<AuthContextValue>({
    isAuthenticated: false,
  });

export function AuthProvider({
  children,
}: PropsWithChildren) {
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: false,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}