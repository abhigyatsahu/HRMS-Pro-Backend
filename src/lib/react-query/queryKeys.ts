// src/lib/react-query/queryKeys.ts

export const QUERY_KEYS = {
     auth: {
    all: ["auth"] as const,

    user: ["auth", "user"] as const,
  },
} as const;