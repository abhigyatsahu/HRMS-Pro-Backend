// src/utils/date/date.util.ts

export function formatDate(
  date: Date | string,
  locale = "en-IN"
): string {
  return new Intl.DateTimeFormat(locale).format(
    new Date(date)
  );
}

export function formatDateTime(
  date: Date | string,
  locale = "en-IN"
): string {
  return new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(date));
}

export function formatTime(
  date: Date | string,
  locale = "en-IN"
): string {
  return new Intl.DateTimeFormat(locale, {
    timeStyle: "short",
  }).format(new Date(date));
}