/**
 * Date helper utilities for reporting periods and filters
 */

/**
 * Returns YYYY-MM string for current month
 */
export function getCurrentMonthString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}`;
}

/**
 * Returns YYYY-MM string for previous month
 */
export function getPreviousMonthString() {
  const now = new Date();
  now.setMonth(now.getMonth() - 1);
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}`;
}

/**
 * Returns formatted month title (e.g., "September 2026")
 */
export function formatMonthTitle(yearMonthString) {
  if (!yearMonthString) return '';
  const [year, month] = yearMonthString.split('-').map(Number);
  const date = new Date(year, month - 1, 1);
  return new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(date);
}

/**
 * Generates array of recent month options for dropdowns (last 12 months)
 */
export function getRecentMonthOptions(count = 12) {
  const options = [];
  const now = new Date();

  for (let i = 0; i < count; i++) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    const label = new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric' }).format(d);
    options.push({ value, label });
  }

  return options;
}
