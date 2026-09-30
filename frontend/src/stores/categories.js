import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../services/api';

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const incomeCategories = computed(() =>
    categories.value.filter((cat) => cat.type === 'INCOME')
  );

  const expenseCategories = computed(() =>
    categories.value.filter((cat) => cat.type === 'EXPENSE')
  );

  async function fetchCategories() {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get('/categories');
      categories.value = response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to load categories';
    } finally {
      isLoading.value = false;
    }
  }

  async function createCategory(categoryData) {
    try {
      const response = await api.post('/categories', categoryData);
      categories.value.push(response.data);
      return { success: true, data: response.data };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to create category';
      return { success: false, error: message };
    }
  }

  async function updateCategory(id, categoryData) {
    try {
      const response = await api.put(`/categories/${id}`, categoryData);
      const index = categories.value.findIndex((c) => c.id === id);
      if (index !== -1) {
        categories.value[index] = response.data;
      }
      return { success: true, data: response.data };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to update category';
      return { success: false, error: message };
    }
  }

  async function deleteCategory(id) {
    try {
      await api.delete(`/categories/${id}`);
      categories.value = categories.value.filter((c) => c.id !== id);
      return { success: true };
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to delete category';
      return { success: false, error: message };
    }
  }

  return {
    categories,
    isLoading,
    error,
    incomeCategories,
    expenseCategories,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory
  };
});
