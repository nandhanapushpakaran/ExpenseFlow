import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';

describe('Auth Pinia Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
  });

  it('initializes with unauthenticated default state', () => {
    const auth = useAuthStore();
    expect(auth.isAuthenticated).toBe(false);
    expect(auth.token).toBeNull();
    expect(auth.user).toBeNull();
    expect(auth.userCurrency).toBe('USD');
  });

  it('logout resets state and clears localStorage', () => {
    const auth = useAuthStore();
    auth.token = 'mock-token';
    auth.user = { id: 1, name: 'Test', preferred_currency: 'EUR' };

    auth.logout();

    expect(auth.isAuthenticated).toBe(false);
    expect(auth.token).toBeNull();
    expect(auth.user).toBeNull();
    expect(localStorage.getItem('token')).toBeNull();
  });
});
