// src/utils/object/object.util.ts

export function isEmpty(
  value: object
) {
  return Object.keys(value).length === 0;
}

export function removeNullValues<
  T extends Record<string, unknown>
>(object: T) {
  return Object.fromEntries(
    Object.entries(object).filter(
      ([, value]) =>
        value !== null &&
        value !== undefined
    )
  );
}