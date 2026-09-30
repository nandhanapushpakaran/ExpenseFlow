/**
 * Currency and number formatters supporting multiple world currencies
 */
export function formatCurrency(amount, currency = 'USD') {
  if (amount === null || amount === undefined || isNaN(amount)) {
    amount = 0;
  }
  const numericAmount = typeof amount === 'string' ? parseFloat(amount) : amount;

  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(numericAmount);
  } catch (e) {
    return `${currency} ${numericAmount.toFixed(2)}`;
  }
}

/**
 * Format date for table and card displays (e.g. Sep 30, 2026)
 */
export function formatDate(dateString) {
  if (!dateString) return '-';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString;

  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(date);
}

/**
 * Format percentage (e.g. 24.5%)
 */
export function formatPercentage(value) {
  if (value === null || value === undefined || isNaN(value)) {
    return '0.0%';
  }
  const numeric = typeof value === 'string' ? parseFloat(value) : value;
  return `${numeric.toFixed(1)}%`;
}

/**
 * Capitalize first letter of string
 */
export function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
