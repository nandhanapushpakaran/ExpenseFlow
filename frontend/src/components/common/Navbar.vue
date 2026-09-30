<template>
  <header class="navbar">
    <div class="navbar-left">
      <button class="mobile-toggle btn-icon" @click="uiStore.toggleSidebar" aria-label="Toggle Menu">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>

    <div class="navbar-right">
      <!-- Theme Toggle -->
      <button class="theme-toggle btn-icon" @click="uiStore.toggleTheme" :title="uiStore.theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
        <svg v-if="uiStore.theme === 'dark'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </button>

      <!-- Currency Badge -->
      <div class="currency-badge" title="Active Preferred Currency">
        <span class="currency-tag">{{ authStore.userCurrency }}</span>
      </div>

      <!-- User Menu -->
      <div class="user-profile">
        <div class="avatar">{{ userInitials }}</div>
        <div class="user-details">
          <span class="user-name">{{ authStore.userName }}</span>
          <span class="user-email">{{ authStore.user?.email }}</span>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useUiStore } from '@/stores/ui';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const uiStore = useUiStore();
const authStore = useAuthStore();

const pageTitle = computed(() => {
  return route.meta?.title || 'Dashboard';
});

const userInitials = computed(() => {
  const name = authStore.userName || 'User';
  return name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2);
});
</script>

<style scoped>
.navbar {
  height: var(--header-height);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 20;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-toggle {
  display: none;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.currency-badge {
  background: var(--bg-surface-hover);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-md);
  font-size: 0.775rem;
  font-weight: 700;
  color: var(--primary-600);
  font-family: var(--font-mono);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-left: 0.5rem;
  border-left: 1px solid var(--border-color);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-500), var(--primary-700));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.2;
}

.user-email {
  font-size: 0.75rem;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .mobile-toggle {
    display: inline-flex;
  }
  .user-details {
    display: none;
  }
}
</style>
