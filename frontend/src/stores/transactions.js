import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../services/api';

export const useTransactionStore = defineStore('transactions', () => {
  const transactions = ref([]);
  const totalCount = ref(0);
  const totalPages = ref(1);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const isLoading = ref(false);
  const error = ref(null);

  // Filters state
  const filters = ref({
    type: '',
    category_id: '',
    start_date: '',
    end_date: '',
    search: '',
    sort_by: 'transaction_date',
    sort_order: 'desc'
  });

  // Dashboard summary data
  const summary = ref({
    total_income: 0,
    total_expenses: 0,
    net_balance: 0,
    savings_rate: 0,
    transaction_count: 0,
    period: '',
    prev_total_income: 0,
    prev_total_expenses: 0,
    income_change_pct: 0,
    expense_change_pct: 0
  });

  const recentTransactions = ref([]);
  const isSummaryLoading = ref(false);

  async function fetchTransactions(page = 1) {
    isLoading.value = true;
    error.value = null;
    currentPage.value = page;

    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      sort_by: filters.value.sort_by,
      sort_order: filters.value.sort_order
    };

    if (filters.value.type) params.type = filters.value.type;
    if (filters.value.category_id) params.category_id = filters.value.category_id;
    if (filters.value.start_date) params.start_date = filters.value.start_date;
    if (filters.value.end_date) params.end_date = filters.value.end_date;
    if (filters.value.search) params.search = filters.value.search;

    try {
      const response = await api.get('/transactions', { params });
      transactions.value = response.data.items;
      totalCount.value = response.data.total;
      totalPages.value = response.data.pages;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch transactions';
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchDashboardSummary(month = null) {
    isSummaryLoading.value = true;
    try {
      const params = month ? { month } : {};
      const response = await api.get('/dashboard/summary', { params });
      summary.value = response.data;
    } catch (err) {
      console.error('Failed to load dashboard summary:', err);
    } finally {
      isSummaryLoading.value = false;
    }
  }

  async function fetchRecentTransactions(limit = 5) {
    try {
      const response = await api.get('/transactions', {
        params: { page: 1, limit, sort_by: 'transaction_date', sort_order: 'desc' }
      });
      recentTransactions.value = response.data.items;
    } catch (err) {
      console.error('Failed to fetch recent transactions:', err);
    }
  }

  async function createTransaction(data) {
    try {
      const response = await api.post('/transactions', data);
      // Refresh current transaction view
      await fetchTransactions(currentPage.value);
      return { success: true, data: response.data };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to add transaction';
      return { success: false, error: message };
    }
  }

  async function updateTransaction(id, data) {
    try {
      const response = await api.put(`/transactions/${id}`, data);
      await fetchTransactions(currentPage.value);
      return { success: true, data: response.data };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to update transaction';
      return { success: false, error: message };
    }
  }

  async function deleteTransaction(id) {
    try {
      await api.delete(`/transactions/${id}`);
      await fetchTransactions(currentPage.value);
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to delete transaction';
      return { success: false, error: message };
    }
  }

  function resetFilters() {
    filters.value = {
      type: '',
      category_id: '',
      start_date: '',
      end_date: '',
      search: '',
      sort_by: 'transaction_date',
      sort_order: 'desc'
    };
    fetchTransactions(1);
  }

  return {
    transactions,
    totalCount,
    totalPages,
    currentPage,
    pageSize,
    isLoading,
    error,
    filters,
    summary,
    recentTransactions,
    isSummaryLoading,
    fetchTransactions,
    fetchDashboardSummary,
    fetchRecentTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    resetFilters
  };
});
