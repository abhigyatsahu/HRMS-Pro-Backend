// src/utils/format/currency.util.ts

export function formatCurrency(
  amount: number,
  currency = "INR",
  locale = "en-IN"
) {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
  }).format(amount);
}