import { describe, it, expect } from 'vitest';
import { formatCurrency, formatDate, formatPercentage, capitalize } from '@/utils/formatters';

describe('formatters utility', () => {
  it('formats currency correctly with USD default', () => {
    const formatted = formatCurrency(1250.5);
    expect(formatted).toContain('1,250.50');
    expect(formatted).toContain('$');
  });

  it('formats currency with EUR correctly', () => {
    const formatted = formatCurrency(200, 'EUR');
    expect(formatted).toContain('200.00');
  });

  it('handles 0, null, or undefined values safely in formatCurrency', () => {
    expect(formatCurrency(0)).toContain('0.00');
    expect(formatCurrency(null)).toContain('0.00');
    expect(formatCurrency(undefined)).toContain('0.00');
    expect(formatCurrency('invalid')).toContain('0.00');
  });

  it('formats date correctly', () => {
    const formatted = formatDate('2026-09-30');
    expect(formatted).toContain('Sep 30, 2026');
  });

  it('handles empty date safely', () => {
    expect(formatDate(null)).toBe('-');
    expect(formatDate('')).toBe('-');
  });

  it('formats percentages correctly', () => {
    expect(formatPercentage(25.46)).toBe('25.5%');
    expect(formatPercentage(0)).toBe('0.0%');
    expect(formatPercentage(null)).toBe('0.0%');
  });

  it('capitalizes string properly', () => {
    expect(capitalize('expense')).toBe('Expense');
    expect(capitalize('INCOME')).toBe('Income');
    expect(capitalize('')).toBe('');
  });
});
