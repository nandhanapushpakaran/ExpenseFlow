<template>
  <div class="card recent-transactions-card">
    <div class="card-header">
      <h3 class="card-title">Recent Transactions</h3>
      <router-link to="/transactions" class="view-all-link">
        <span>View all</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </router-link>
    </div>

    <div v-if="transactions.length === 0" class="empty-state">
      <p>No recent transactions</p>
    </div>

    <div v-else class="transactions-list">
      <div
        v-for="tx in transactions"
        :key="tx.id"
        class="transaction-row"
      >
        <div class="tx-left">
          <div class="tx-dot" :class="[tx.type === 'INCOME' ? 'dot-income' : 'dot-expense']"></div>
          <div class="tx-info">
            <span class="tx-desc">{{ tx.description }}</span>
            <div class="tx-meta">
              <span class="tx-cat" :style="{ color: tx.category?.color }">
                {{ tx.category?.name || 'Uncategorized' }}
              </span>
              <span class="tx-divider">•</span>
              <span class="tx-date">{{ formatDate(tx.transaction_date) }}</span>
            </div>
          </div>
        </div>
        <div class="tx-right">
          <span
            class="tx-amount font-mono font-bold"
            :class="[tx.type === 'INCOME' ? 'text-income' : 'text-expense']"
          >
            {{ tx.type === 'INCOME' ? '+' : '-' }}{{ formatCurrency(tx.amount, authStore.userCurrency) }}
          </span>
        </div>
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
  }
});

const authStore = useAuthStore();
</script>

<style scoped>
.recent-transactions-card {
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--primary-500);
}

.transactions-list {
  display: flex;
  flex-direction: column;
}

.transaction-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--border-color);
}

.transaction-row:last-child {
  border-bottom: none;
}

.tx-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.tx-dot {
  width: 10px;
  height: 10px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.dot-income {
  background-color: var(--income-500);
}

.dot-expense {
  background-color: var(--expense-500);
}

.tx-info {
  display: flex;
  flex-direction: column;
}

.tx-desc {
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.925rem;
}

.tx-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.775rem;
  color: var(--text-muted);
}

.tx-divider {
  color: var(--text-subtle);
}

.tx-amount {
  font-size: 0.95rem;
}

.empty-state {
  padding: 2rem 0;
  text-align: center;
  color: var(--text-muted);
}
</style>
