<template>
  <div>
    <!-- Backdrop for mobile drawer -->
    <div
      v-if="uiStore.isSidebarOpen"
      class="sidebar-backdrop"
      @click="uiStore.closeSidebar"
    ></div>

    <aside class="sidebar" :class="{ 'sidebar-open': uiStore.isSidebarOpen }">
      <!-- App Brand / Logo -->
      <div class="sidebar-brand">
        <div class="brand-logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12V7H5a2 2 0 0 1 0-4h14v4" />
            <path d="M3 5v14a2 2 0 0 0 2 2h16v-5" />
            <path d="M18 12a2 2 0 0 0 0 4h4v-4Z" />
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-name">ExpenseFlow</span>
          <span class="brand-badge">PRO</span>
        </div>
      </div>

      <!-- Quick Action Button -->
      <div class="sidebar-action">
        <button class="btn btn-primary quick-add-btn" @click="emit('quick-add')">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <span>New Transaction</span>
        </button>
      </div>

      <!-- Navigation Links -->
      <nav class="sidebar-nav">
        <router-link
          to="/dashboard"
          class="nav-item"
          @click="uiStore.closeSidebar"
        >
          <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="9"></rect>
            <rect x="14" y="3" width="7" height="5"></rect>
            <rect x="14" y="12" width="7" height="9"></rect>
            <rect x="3" y="16" width="7" height="5"></rect>
          </svg>
          <span>Dashboard</span>
        </router-link>

        <router-link
          to="/transactions"
          class="nav-item"
          @click="uiStore.closeSidebar"
        >
          <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="1" x2="12" y2="23"></line>
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          <span>Transactions</span>
        </router-link>

        <router-link
          to="/categories"
          class="nav-item"
          @click="uiStore.closeSidebar"
        >
          <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Categories</span>
        </router-link>

        <router-link
          to="/reports"
          class="nav-item"
          @click="uiStore.closeSidebar"
        >
          <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v18h18"></path>
            <path d="m19 9-5 5-4-4-3 3"></path>
          </svg>
          <span>Reports</span>
        </router-link>

        <router-link
          to="/settings"
          class="nav-item"
          @click="uiStore.closeSidebar"
        >
          <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
          <span>Settings</span>
        </router-link>
      </nav>

      <!-- Sidebar Footer / Logout -->
      <div class="sidebar-footer">
        <button class="logout-btn" @click="handleLogout">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUiStore } from '@/stores/ui';
import { useAuthStore } from '@/stores/auth';

const emit = defineEmits(['quick-add']);
const router = useRouter();
const uiStore = useUiStore();
const authStore = useAuthStore();

function handleLogout() {
  authStore.logout();
  uiStore.closeSidebar();
  router.push('/login');
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  z-index: 30;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-brand {
  height: var(--header-height);
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid var(--border-color);
}

.brand-logo {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, var(--primary-600), var(--primary-500));
  color: #ffffff;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.25);
}

.brand-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.brand-name {
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-main);
}

.brand-badge {
  font-size: 0.65rem;
  font-weight: 800;
  background: var(--primary-50);
  color: var(--primary-600);
  padding: 0.15rem 0.4rem;
  border-radius: var(--radius-sm);
}

.sidebar-action {
  padding: 1.25rem 1.25rem 0.5rem;
}

.quick-add-btn {
  width: 100%;
  padding: 0.75rem;
  font-size: 0.9rem;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.7rem 1rem;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.925rem;
  transition: var(--transition);
}

.nav-item:hover {
  color: var(--text-main);
  background: var(--bg-surface-hover);
}

.nav-item.router-link-active {
  color: var(--primary-600);
  background: var(--primary-50);
}

[data-theme='dark'] .nav-item.router-link-active {
  background: rgba(99, 102, 241, 0.15);
  color: var(--primary-400);
}

.nav-icon {
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 1.25rem;
  border-top: 1px solid var(--border-color);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  border-radius: var(--radius-md);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.9rem;
  transition: var(--transition);
}

.logout-btn:hover {
  background: var(--expense-50);
  color: var(--expense-600);
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar.sidebar-open {
    transform: translateX(0);
  }
  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: var(--modal-backdrop);
    backdrop-filter: blur(2px);
    z-index: 25;
  }
}
</style>
