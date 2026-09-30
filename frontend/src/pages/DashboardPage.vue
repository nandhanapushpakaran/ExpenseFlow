<template>
  <div class="dashboard-page">
    <!-- Header Controls: Welcome + Month Selector + Quick Actions -->
    <div class="dashboard-header">
      <div class="welcome-box">
        <h2 class="welcome-title">Hello, {{ authStore.userName }} 👋</h2>
        <p class="welcome-subtitle">Here is your financial activity and spending overview.</p>
      </div>

      <div class="header-actions">
        <!-- Month Selector Dropdown -->
        <div class="period-selector">
          <select v-model="selectedMonth" @change="handlePeriodChange">
            <option
              v-for="opt in monthOptions"
              :key="opt.value"
              :value="opt.value"
            >
              {{ opt.label }}
            </option>
          </select>
        </div>

        <!-- Quick Add Buttons -->
        <div class="quick-btns">
          <button class="btn btn-success btn-sm" @click="$emit('open-add-transaction', 'INCOME')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span>Add Income</span>
          </button>
          <button class="btn btn-danger btn-sm" @click="$emit('open-add-transaction', 'EXPENSE')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span>Add Expense</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Summary Stat Cards Grid -->
    <div class="stats-grid">
      <StatCard
        title="Total Income"
        :value="summary.total_income"
        variant="income"
        :change-pct="summary.income_change_pct"
        subtext="vs last month"
      >
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
          </svg>
        </template>
      </StatCard>

      <StatCard
        title="Total Expenses"
        :value="summary.total_expenses"
        variant="expense"
        :change-pct="summary.expense_change_pct"
        subtext="vs last month"
      >
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="19 12 12 19 5 12"></polyline>
          </svg>
        </template>
      </StatCard>

      <StatCard
        title="Remaining Balance"
        :value="summary.net_balance"
        :variant="summary.net_balance >= 0 ? 'primary' : 'expense'"
        :subtext="summary.net_balance >= 0 ? 'Positive net cashflow' : 'Deficit this period'"
      >
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
        </template>
      </StatCard>

      <StatCard
        title="Savings Rate"
        :value="summary.savings_rate"
        type="percentage"
        variant="info"
        :subtext="`${summary.transaction_count} transactions recorded`"
      >
        <template #icon>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
          </svg>
        </template>
      </StatCard>
    </div>

    <!-- Charts Section -->
    <div class="charts-grid">
      <!-- Income vs Expense Bar Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Income vs Expenses</h3>
          <span class="card-subtitle">Monthly Overview</span>
        </div>
        <IncomeExpenseChart :monthly-data="monthlyChartData" />
      </div>

      <!-- Category Breakdown Donut Chart -->
      <div class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Expense by Category</h3>
          <span class="card-subtitle">{{ selectedMonthTitle }}</span>
        </div>
        <CategoryDonutChart :categories="categoryBreakdownData" />
      </div>
    </div>

    <!-- Bottom Row: Spending Trend & Recent Transactions -->
    <div class="bottom-grid">
      <div class="card chart-card">
        <div class="card-header">
          <h3 class="card-title">Monthly Spending Trend</h3>
          <span class="card-subtitle">Cumulative Expenses</span>
        </div>
        <SpendingTrendChart :trend-data="spendingTrendData" />
      </div>

      <RecentTransactions :transactions="recentTransactions" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import StatCard from '@/components/common/StatCard.vue';
import IncomeExpenseChart from '@/components/charts/IncomeExpenseChart.vue';
import CategoryDonutChart from '@/components/charts/CategoryDonutChart.vue';
import SpendingTrendChart from '@/components/charts/SpendingTrendChart.vue';
import RecentTransactions from '@/components/dashboard/RecentTransactions.vue';
import { useAuthStore } from '@/stores/auth';
import { useTransactionStore } from '@/stores/transactions';
import { useCategoryStore } from '@/stores/categories';
import { getCurrentMonthString, getRecentMonthOptions, formatMonthTitle } from '@/utils/date';
import api from '@/services/api';

defineEmits(['open-add-transaction']);

const authStore = useAuthStore();
const transactionStore = useTransactionStore();
const categoryStore = useCategoryStore();

const selectedMonth = ref(getCurrentMonthString());
const monthOptions = getRecentMonthOptions(12);

const monthlyChartData = ref([]);
const categoryBreakdownData = ref([]);
const spendingTrendData = ref([]);

const summary = computed(() => transactionStore.summary);
const recentTransactions = computed(() => transactionStore.recentTransactions);
const selectedMonthTitle = computed(() => formatMonthTitle(selectedMonth.value));

async function loadDashboardData() {
  await Promise.all([
    transactionStore.fetchDashboardSummary(selectedMonth.value),
    transactionStore.fetchRecentTransactions(5),
    categoryStore.fetchCategories(),
    fetchChartsData()
  ]);
}

async function fetchChartsData() {
  try {
    const [monthlyRes, categoryRes, trendsRes] = await Promise.all([
      api.get('/dashboard/monthly', { params: { months: 6 } }),
      api.get('/dashboard/category-breakdown', { params: { month: selectedMonth.value } }),
      api.get('/dashboard/trends', { params: { months: 6 } })
    ]);

    monthlyChartData.value = monthlyRes.data || [];
    categoryBreakdownData.value = categoryRes.data || [];
    spendingTrendData.value = trendsRes.data || [];
  } catch (err) {
    console.error('Failed to load dashboard chart data:', err);
  }
}

function handlePeriodChange() {
  loadDashboardData();
}

onMounted(() => {
  loadDashboardData();
});
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.25rem;
}

.welcome-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.welcome-subtitle {
  font-size: 0.925rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.period-selector select {
  padding: 0.55rem 0.85rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.quick-btns {
  display: flex;
  gap: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 1.25rem;
}

.bottom-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.chart-card {
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
}

.card-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .charts-grid {
    grid-template-columns: 1fr;
  }
  .bottom-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
