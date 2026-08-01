// src/utils/format/string.util.ts

export function capitalize(value: string) {
  if (!value) return "";

  return (
    value.charAt(0).toUpperCase() +
    value.slice(1)
  );
}

export function initials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

export function truncate(
  value: string,
  length = 50
) {
  if (value.length <= length) {
    return value;
  }

  return `${value.substring(0, length)}...`;
}