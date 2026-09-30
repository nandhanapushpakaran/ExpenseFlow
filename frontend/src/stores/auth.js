import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null);
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const isLoading = ref(false);
  const error = ref(null);

  const isAuthenticated = computed(() => !!token.value);
  const userCurrency = computed(() => user.value?.preferred_currency || 'USD');
  const userName = computed(() => user.value?.name || 'User');

  async function login(email, password) {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token, user: userData } = response.data;

      token.value = access_token;
      user.value = userData;

      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Invalid email or password';
      error.value = message;
      return { success: false, error: message };
    } finally {
      isLoading.value = false;
    }
  }

  async function register(userData) {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.post('/auth/register', userData);
      const { access_token, user: newUser } = response.data;

      token.value = access_token;
      user.value = newUser;

      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(newUser));

      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Registration failed';
      error.value = message;
      return { success: false, error: message };
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return;
    try {
      const response = await api.get('/auth/me');
      user.value = response.data;
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch (err) {
      logout();
    }
  }

  async function updateProfile(data) {
    isLoading.value = true;
    try {
      const response = await api.patch('/auth/profile', data);
      user.value = response.data;
      localStorage.setItem('user', JSON.stringify(response.data));
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Profile update failed';
      return { success: false, error: message };
    } finally {
      isLoading.value = false;
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    userCurrency,
    userName,
    login,
    register,
    fetchCurrentUser,
    updateProfile,
    logout
  };
});
