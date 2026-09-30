<template>
  <div class="reports-page">
    <div class="page-header">
      <div>
        <h2 class="page-title">Financial Reports</h2>
        <p class="page-subtitle">Detailed breakdown and exportable insights on your financial flow</p>
      </div>

      <div class="header-actions">
        <select v-model="selectedMonth" @change="loadReportData">
          <option
            v-for="opt in monthOptions"
            :key="opt.value"
            :value="opt.value"
          >
            {{ opt.label }}
          </option>
        </select>
        <button class="btn btn-secondary" @click="exportToCSV">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          <span>Export CSV</span>
        </button>
      </div>
    </div>

    <!-- Monthly Summary Overview Table -->
    <div class="card report-section">
      <h3 class="section-title">Monthly Performance Summary ({{ selectedMonthTitle }})</h3>
      <div class="summary-table-container">
        <table>
          <thead>
            <tr>
              <th>Metric</th>
              <th>Current Period</th>
              <th>Previous Period</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="font-bold">Total Income</td>
              <td class="text-income font-mono font-bold">{{ formatCurrency(summary.total_income, authStore.userCurrency) }}</td>
              <td class="font-mono text-muted">{{ formatCurrency(summary.prev_total_income, authStore.userCurrency) }}</td>
              <td>
                <span class="badge" :class="[summary.income_change_pct >= 0 ? 'badge-income' : 'badge-expense']">
                  {{ summary.income_change_pct >= 0 ? '+' : '' }}{{ summary.income_change_pct.toFixed(1) }}%
                </span>
              </td>
            </tr>
            <tr>
              <td class="font-bold">Total Expenses</td>
              <td class="text-expense font-mono font-bold">{{ formatCurrency(summary.total_expenses, authStore.userCurrency) }}</td>
              <td class="font-mono text-muted">{{ formatCurrency(summary.prev_total_expenses, authStore.userCurrency) }}</td>
              <td>
                <span class="badge" :class="[summary.expense_change_pct <= 0 ? 'badge-income' : 'badge-expense']">
                  {{ summary.expense_change_pct >= 0 ? '+' : '' }}{{ summary.expense_change_pct.toFixed(1) }}%
                </span>
              </td>
            </tr>
            <tr>
              <td class="font-bold">Net Balance</td>
              <td class="font-mono font-bold" :class="[summary.net_balance >= 0 ? 'text-income' : 'text-expense']">
                {{ formatCurrency(summary.net_balance, authStore.userCurrency) }}
              </td>
              <td class="font-mono text-muted">
                {{ formatCurrency(summary.prev_total_income - summary.prev_total_expenses, authStore.userCurrency) }}
              </td>
              <td>
                <span class="badge" :class="[summary.net_balance >= 0 ? 'badge-income' : 'badge-expense']">
                  {{ summary.net_balance >= 0 ? 'SURPLUS' : 'DEFICIT' }}
                </span>
              </td>
            </tr>
            <tr>
              <td class="font-bold">Savings Rate</td>
              <td class="font-mono font-bold">{{ formatPercentage(summary.savings_rate) }}</td>
              <td class="font-mono text-muted">-</td>
              <td>
                <span class="badge badge-income" v-if="summary.savings_rate > 20">HEALTHY (>20%)</span>
                <span class="badge badge-expense" v-else>ATTENTION</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Category Spending Breakdown Table -->
    <div class="card report-section">
      <h3 class="section-title">Expense Distribution by Category</h3>
      <div v-if="categoriesBreakdown.length === 0" class="empty-state">
        <p>No expense data recorded for {{ selectedMonthTitle }}</p>
      </div>
      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th style="text-align: right;">Amount Spent</th>
              <th style="text-align: right;">Share of Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cat in categoriesBreakdown" :key="cat.name">
              <td>
                <span class="category-name-badge">
                  <span class="cat-dot" :style="{ backgroundColor: cat.color || '#6366f1' }"></span>
                  {{ cat.name }}
                </span>
              </td>
              <td style="text-align: right;" class="font-mono font-bold text-expense">
                {{ formatCurrency(cat.total_amount, authStore.userCurrency) }}
              </td>
              <td style="text-align: right;" class="font-mono">
                {{ formatPercentage(cat.percentage) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTransactionStore } from '@/stores/transactions';
import { getCurrentMonthString, getRecentMonthOptions, formatMonthTitle } from '@/utils/date';
import { formatCurrency, formatPercentage } from '@/utils/formatters';
import api from '@/services/api';

const authStore = useAuthStore();
const transactionStore = useTransactionStore();

const selectedMonth = ref(getCurrentMonthString());
const monthOptions = getRecentMonthOptions(12);

const summary = computed(() => transactionStore.summary);
const selectedMonthTitle = computed(() => formatMonthTitle(selectedMonth.value));
const categoriesBreakdown = ref([]);

async function loadReportData() {
  await transactionStore.fetchDashboardSummary(selectedMonth.value);
  try {
    const res = await api.get('/dashboard/category-breakdown', {
      params: { month: selectedMonth.value }
    });
    categoriesBreakdown.value = res.data || [];
  } catch (err) {
    console.error('Failed to load category breakdown for reports:', err);
  }
}

async function exportToCSV() {
  try {
    const res = await api.get('/transactions', {
      params: { limit: 1000, page: 1, sort_by: 'transaction_date', sort_order: 'desc' }
    });
    const items = res.data.items || [];
    if (items.length === 0) {
      alert('No transactions to export');
      return;
    }

    const headers = ['Date', 'Type', 'Category', 'Description', 'Amount', 'Payment Method', 'Notes'];
    const rows = items.map((t) => [
      t.transaction_date.slice(0, 10),
      t.type,
      `"${(t.category?.name || 'Uncategorized').replace(/"/g, '""')}"`,
      `"${(t.description || '').replace(/"/g, '""')}"`,
      t.amount,
      `"${(t.payment_method || '').replace(/"/g, '""')}"`,
      `"${(t.notes || '').replace(/"/g, '""')}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `Expense_Report_${selectedMonth.value}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    alert('Failed to export CSV: ' + err.message);
  }
}

onMounted(() => {
  loadReportData();
});
</script>

<style scoped>
.reports-page {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-actions select {
  padding: 0.55rem 0.85rem;
  font-weight: 600;
}

.report-section {
  display: flex;
  flex-direction: column;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 1.25rem;
}

.category-name-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.cat-dot {
  width: 9px;
  height: 9px;
  border-radius: var(--radius-full);
}
</style>
