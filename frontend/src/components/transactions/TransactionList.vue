<template>
  <div class="transaction-list-wrapper">
    <!-- Empty State -->
    <div v-if="!isLoading && transactions.length === 0" class="card empty-state">
      <div class="empty-state-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M16 16s-1.5-2-4-2-4 2-4 2"></path>
          <line x1="9" y1="9" x2="9.01" y2="9"></line>
          <line x1="15" y1="9" x2="15.01" y2="9"></line>
        </svg>
      </div>
      <h3 class="empty-state-title">No transactions found</h3>
      <p class="empty-state-description">
        No records match your selected filters. Try broadening your search or add a new transaction.
      </p>
      <button class="btn btn-primary btn-sm" @click="$emit('add-transaction')">
        Add Transaction
      </button>
    </div>

    <!-- Table of Transactions -->
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Type</th>
            <th>Category</th>
            <th>Description</th>
            <th>Method</th>
            <th style="text-align: right;">Amount</th>
            <th style="text-align: right;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in transactions" :key="tx.id">
            <td class="font-mono text-muted">{{ formatDate(tx.transaction_date) }}</td>
            <td>
              <span class="badge" :class="[tx.type === 'INCOME' ? 'badge-income' : 'badge-expense']">
                {{ tx.type }}
              </span>
            </td>
            <td>
              <span class="category-tag" :style="{ borderColor: tx.category?.color || '#94a3b8' }">
                <span class="cat-dot" :style="{ backgroundColor: tx.category?.color || '#94a3b8' }"></span>
                {{ tx.category?.name || 'Uncategorized' }}
              </span>
            </td>
            <td class="description-cell">
              <div class="desc-title">{{ tx.description }}</div>
              <div v-if="tx.notes" class="desc-notes text-muted" :title="tx.notes">
                {{ tx.notes }}
              </div>
            </td>
            <td>
              <span class="method-tag">{{ tx.payment_method || 'Other' }}</span>
            </td>
            <td class="amount-cell" :class="[tx.type === 'INCOME' ? 'text-income' : 'text-expense']">
              <span class="font-mono font-bold">
                {{ tx.type === 'INCOME' ? '+' : '-' }}{{ formatCurrency(tx.amount, authStore.userCurrency) }}
              </span>
            </td>
            <td class="actions-cell">
              <button
                class="btn-icon btn-sm"
                title="Edit Transaction"
                @click="$emit('edit', tx)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </button>
              <button
                class="btn-icon btn-sm delete-btn"
                title="Delete Transaction"
                @click="$emit('delete', tx)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Controls -->
    <div v-if="totalPages > 1" class="pagination-bar">
      <div class="pagination-info text-muted">
        Showing Page {{ currentPage }} of {{ totalPages }} ({{ totalCount }} total records)
      </div>
      <div class="pagination-actions">
        <button
          class="btn btn-secondary btn-sm"
          :disabled="currentPage <= 1"
          @click="$emit('page-change', currentPage - 1)"
        >
          Previous
        </button>
        <button
          class="btn btn-secondary btn-sm"
          :disabled="currentPage >= totalPages"
          @click="$emit('page-change', currentPage + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate, formatCurrency } from '@/utils/formatters';
import { useAuthStore } from '@/stores/auth';

defineProps({
  transactions: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 1
  },
  totalCount: {
    type: Number,
    default: 0
  }
});

defineEmits(['edit', 'delete', 'page-change', 'add-transaction']);

const authStore = useAuthStore();
</script>

<style scoped>
.category-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-sm);
  background: var(--bg-app);
  border: 1px solid transparent;
}

.cat-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
}

.description-cell {
  max-width: 260px;
}

.desc-title {
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.desc-notes {
  font-size: 0.775rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.method-tag {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.amount-cell {
  text-align: right;
  font-size: 1rem;
}

.actions-cell {
  text-align: right;
  white-space: nowrap;
}

.delete-btn:hover {
  color: var(--expense-500);
}

.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.25rem;
  padding: 0 0.5rem;
}

.pagination-info {
  font-size: 0.875rem;
}

.pagination-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
