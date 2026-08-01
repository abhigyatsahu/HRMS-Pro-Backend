// src/providers/ThemeProvider.tsx

import type { PropsWithChildren } from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

import { THEME } from "@/config/theme";

export function ThemeProvider({
  children,
}: PropsWithChildren) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme={THEME.DEFAULT}
      enableSystem
      storageKey={THEME.STORAGE_KEY}
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  );
}