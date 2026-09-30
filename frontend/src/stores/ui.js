import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
  // Theme state (check localStorage or system preference)
  const savedTheme = localStorage.getItem('theme') || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  
  const theme = ref(savedTheme);
  const isSidebarOpen = ref(false);
  const toasts = ref([]);

  // Apply theme to HTML attribute
  function applyTheme(newTheme) {
    theme.value = newTheme;
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  }

  // Toggle theme between light and dark
  function toggleTheme() {
    const nextTheme = theme.value === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  }

  // Initialize theme on app load
  function initTheme() {
    applyTheme(theme.value);
  }

  // Sidebar toggle for mobile
  function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value;
  }

  function closeSidebar() {
    isSidebarOpen.value = false;
  }

  // Toast notifications
  function addToast({ message, type = 'info', duration = 3500 }) {
    const id = Date.now() + Math.random();
    toasts.value.push({ id, message, type });
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  }

  function removeToast(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }

  return {
    theme,
    isSidebarOpen,
    toasts,
    initTheme,
    toggleTheme,
    toggleSidebar,
    closeSidebar,
    addToast,
    removeToast
  };
});
