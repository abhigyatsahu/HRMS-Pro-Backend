// src/utils/query/query.util.ts

export function buildQueryString(
  params: Record<string, unknown>
) {
  const searchParams =
    new URLSearchParams();

  Object.entries(params).forEach(
    ([key, value]) => {
      if (
        value !== null &&
        value !== undefined &&
        value !== ""
      ) {
        searchParams.append(
          key,
          String(value)
        );
      }
    }
  );

  return searchParams.toString();
}