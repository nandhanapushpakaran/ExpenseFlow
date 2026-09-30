<template>
  <div class="transactions-page">
    <div class="page-header">
      <div>
        <h2 class="page-title">Transactions</h2>
        <p class="page-subtitle">View, search, and manage all your financial records</p>
      </div>
      <button class="btn btn-primary" @click="openCreateModal">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        <span>Add Transaction</span>
      </button>
    </div>

    <!-- Filters Component -->
    <TransactionFilters
      :filters="transactionStore.filters"
      @update-filters="handleUpdateFilters"
      @reset-filters="handleResetFilters"
    />

    <!-- Transactions List Component -->
    <TransactionList
      :transactions="transactionStore.transactions"
      :is-loading="transactionStore.isLoading"
      :current-page="transactionStore.currentPage"
      :total-pages="transactionStore.totalPages"
      :total-count="transactionStore.totalCount"
      @edit="openEditModal"
      @delete="confirmDelete"
      @page-change="handlePageChange"
      @add-transaction="openCreateModal"
    />

    <!-- Add/Edit Transaction Form Modal -->
    <TransactionForm
      :is-open="isFormModalOpen"
      :transaction="selectedTransaction"
      @close="closeFormModal"
      @submit="handleFormSubmit"
    />

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :is-open="isConfirmOpen"
      title="Delete Transaction"
      :message="deleteMessage"
      confirm-text="Delete Transaction"
      :is-loading="isDeleting"
      @confirm="executeDelete"
      @cancel="isConfirmOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import TransactionFilters from '@/components/transactions/TransactionFilters.vue';
import TransactionList from '@/components/transactions/TransactionList.vue';
import TransactionForm from '@/components/transactions/TransactionForm.vue';
import ConfirmDialog from '@/components/common/ConfirmDialog.vue';
import { useTransactionStore } from '@/stores/transactions';
import { useCategoryStore } from '@/stores/categories';
import { useUiStore } from '@/stores/ui';
import { formatCurrency } from '@/utils/formatters';
import { useAuthStore } from '@/stores/auth';

const transactionStore = useTransactionStore();
const categoryStore = useCategoryStore();
const uiStore = useUiStore();
const authStore = useAuthStore();

const isFormModalOpen = ref(false);
const selectedTransaction = ref(null);

const isConfirmOpen = ref(false);
const transactionToDelete = ref(null);
const isDeleting = ref(false);

const deleteMessage = computed(() => {
  if (!transactionToDelete.value) return '';
  const amountStr = formatCurrency(transactionToDelete.value.amount, authStore.userCurrency);
  return `Are you sure you want to permanently delete "${transactionToDelete.value.description}" (${amountStr})?`;
});

function openCreateModal() {
  selectedTransaction.value = null;
  isFormModalOpen.value = true;
}

function openEditModal(tx) {
  selectedTransaction.value = tx;
  isFormModalOpen.value = true;
}

function closeFormModal() {
  isFormModalOpen.value = false;
  selectedTransaction.value = null;
}

async function handleFormSubmit(formData, callback) {
  let result;
  if (selectedTransaction.value?.id) {
    result = await transactionStore.updateTransaction(selectedTransaction.value.id, formData);
  } else {
    result = await transactionStore.createTransaction(formData);
  }

  if (result.success) {
    uiStore.addToast({
      message: selectedTransaction.value?.id ? 'Transaction updated successfully' : 'Transaction created successfully',
      type: 'success'
    });
    callback(null);
  } else {
    callback(result.error);
  }
}

function confirmDelete(tx) {
  transactionToDelete.value = tx;
  isConfirmOpen.value = true;
}

async function executeDelete() {
  if (!transactionToDelete.value) return;
  isDeleting.value = true;
  const result = await transactionStore.deleteTransaction(transactionToDelete.value.id);
  isDeleting.value = false;
  isConfirmOpen.value = false;

  if (result.success) {
    uiStore.addToast({
      message: 'Transaction deleted successfully',
      type: 'success'
    });
  } else {
    uiStore.addToast({
      message: result.error,
      type: 'error'
    });
  }
}

function handleUpdateFilters(newFilters) {
  transactionStore.filters = { ...transactionStore.filters, ...newFilters };
  transactionStore.fetchTransactions(1);
}

function handleResetFilters() {
  transactionStore.resetFilters();
}

function handlePageChange(newPage) {
  transactionStore.fetchTransactions(newPage);
}

onMounted(async () => {
  await Promise.all([
    categoryStore.fetchCategories(),
    transactionStore.fetchTransactions(1)
  ]);
});
</script>

<style scoped>
.transactions-page {
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.925rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}
</style>
