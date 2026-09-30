<template>
  <div class="auth-layout">
    <div class="auth-top-bar">
      <div class="brand">
        <div class="brand-logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12V7H5a2 2 0 0 1 0-4h14v4" />
            <path d="M3 5v14a2 2 0 0 0 2 2h16v-5" />
            <path d="M18 12a2 2 0 0 0 0 4h4v-4Z" />
          </svg>
        </div>
        <span class="brand-name">ExpenseFlow</span>
      </div>

      <button class="theme-toggle btn-icon" @click="uiStore.toggleTheme">
        <svg v-if="uiStore.theme === 'dark'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </button>
    </div>

    <div class="auth-center-container">
      <router-view />
    </div>

    <footer class="auth-footer">
      <p>© 2026 Expense Tracker Dashboard — Built for technical portfolio demonstration</p>
    </footer>
  </div>
</template>

<script setup>
import { useUiStore } from '@/stores/ui';

const uiStore = useUiStore();
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-app);
  padding: 1.5rem;
}

.auth-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-logo {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary-600), var(--primary-500));
  color: #ffffff;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-main);
}

.auth-center-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.auth-footer {
  text-align: center;
  font-size: 0.8rem;
  color: var(--text-muted);
  padding-top: 1rem;
}
</style>
