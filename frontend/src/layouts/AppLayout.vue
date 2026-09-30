<template>
  <div class="app-layout">
    <Sidebar @quick-add="openQuickAdd" />
    
    <div class="main-wrapper">
      <Navbar />

      <main class="page-content">
        <router-view @open-add-transaction="openQuickAdd" />
      </main>
    </div>

    <!-- Quick Add Transaction Modal -->
    <TransactionForm
      :is-open="isQuickAddOpen"
      :default-type="quickAddType"
      @close="isQuickAddOpen = false"
      @submit="handleQuickAddSubmit"
    />

    <!-- Global Toast Container -->
    <div class="toast-container">
      <div
        v-for="toast in uiStore.toasts"
        :key="toast.id"
        class="toast-card"
        :class="[`toast-${toast.type}`]"
      >
        <span>{{ toast.message }}</span>
        <button class="toast-close" @click="uiStore.removeToast(toast.id)">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Sidebar from '@/components/common/Sidebar.vue';
import Navbar from '@/components/common/Navbar.vue';
import TransactionForm from '@/components/transactions/TransactionForm.vue';
import { useUiStore } from '@/stores/ui';
import { useTransactionStore } from '@/stores/transactions';

const uiStore = useUiStore();
const transactionStore = useTransactionStore();

const isQuickAddOpen = ref(false);
const quickAddType = ref('EXPENSE');

function openQuickAdd(type = 'EXPENSE') {
  quickAddType.value = type;
  isQuickAddOpen.value = true;
}

async function handleQuickAddSubmit(formData, callback) {
  const result = await transactionStore.createTransaction(formData);
  if (result.success) {
    uiStore.addToast({
      message: `${formData.type === 'INCOME' ? 'Income' : 'Expense'} recorded successfully!`,
      type: 'success'
    });
    // Also refresh dashboard summary
    await transactionStore.fetchDashboardSummary();
    await transactionStore.fetchRecentTransactions();
    callback(null);
  } else {
    callback(result.error);
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-app);
}

.main-wrapper {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  transition: margin-left 0.3s ease;
}

.page-content {
  flex: 1;
  padding: 1.75rem 2rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

/* Toast Container */
.toast-container {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 9999;
}

.toast-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15);
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  animation: slideIn 0.25s ease-out;
}

.toast-success { background-color: var(--income-500); }
.toast-error { background-color: var(--expense-500); }
.toast-info { background-color: var(--primary-600); }

.toast-close {
  font-size: 1.15rem;
  line-height: 1;
  color: #ffffff;
  opacity: 0.8;
  cursor: pointer;
}

@keyframes slideIn {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .main-wrapper {
    margin-left: 0;
  }
  .page-content {
    padding: 1.25rem 1rem;
  }
}
</style>
