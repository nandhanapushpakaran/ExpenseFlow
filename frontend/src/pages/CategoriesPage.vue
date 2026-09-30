<template>
  <div class="categories-page">
    <div class="page-header">
      <div>
        <h2 class="page-title">Category Management</h2>
        <p class="page-subtitle">Organize and customize your income and expense categories</p>
      </div>
      <button class="btn btn-primary" @click="openCreateModal">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        <span>Add Category</span>
      </button>
    </div>

    <!-- Category Type Tabs -->
    <div class="tabs-header">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'EXPENSE' }"
        @click="activeTab = 'EXPENSE'"
      >
        Expense Categories ({{ expenseCategories.length }})
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'INCOME' }"
        @click="activeTab = 'INCOME'"
      >
        Income Categories ({{ incomeCategories.length }})
      </button>
    </div>

    <!-- Categories Grid -->
    <div class="categories-grid">
      <div
        v-for="cat in displayedCategories"
        :key="cat.id"
        class="card category-card"
      >
        <div class="category-main">
          <div class="category-icon-box" :style="{ backgroundColor: cat.color || '#6366f1' }">
            <span class="cat-letter">{{ cat.name.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="category-info">
            <div class="cat-title-row">
              <h4 class="cat-name">{{ cat.name }}</h4>
              <span v-if="cat.is_default" class="badge-default">SYSTEM</span>
            </div>
            <span class="cat-meta">{{ cat.type }} Category</span>
          </div>
        </div>

        <div class="category-actions">
          <button
            class="btn-icon btn-sm"
            title="Edit Category"
            @click="openEditModal(cat)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
          <button
            v-if="!cat.is_default"
            class="btn-icon btn-sm delete-btn"
            title="Delete Category"
            @click="confirmDelete(cat)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Category Modal -->
    <CategoryModal
      :is-open="isModalOpen"
      :category="selectedCategory"
      :default-type="activeTab"
      @close="closeModal"
      @submit="handleCategorySubmit"
    />

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      :is-open="isConfirmOpen"
      title="Delete Category"
      :message="`Are you sure you want to delete category '${categoryToDelete?.name}'? This cannot be deleted if transactions are currently assigned to it.`"
      confirm-text="Delete Category"
      :is-loading="isDeleting"
      @confirm="executeDelete"
      @cancel="isConfirmOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CategoryModal from '@/components/categories/CategoryModal.vue';
import ConfirmDialog from '@/components/common/ConfirmDialog.vue';
import { useCategoryStore } from '@/stores/categories';
import { useUiStore } from '@/stores/ui';

const categoryStore = useCategoryStore();
const uiStore = useUiStore();

const activeTab = ref('EXPENSE');
const isModalOpen = ref(false);
const selectedCategory = ref(null);

const isConfirmOpen = ref(false);
const categoryToDelete = ref(null);
const isDeleting = ref(false);

const expenseCategories = computed(() => categoryStore.expenseCategories);
const incomeCategories = computed(() => categoryStore.incomeCategories);

const displayedCategories = computed(() => {
  return activeTab.value === 'EXPENSE' ? expenseCategories.value : incomeCategories.value;
});

function openCreateModal() {
  selectedCategory.value = null;
  isModalOpen.value = true;
}

function openEditModal(cat) {
  selectedCategory.value = cat;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  selectedCategory.value = null;
}

async function handleCategorySubmit(formData, callback) {
  let result;
  if (selectedCategory.value?.id) {
    result = await categoryStore.updateCategory(selectedCategory.value.id, formData);
  } else {
    result = await categoryStore.createCategory(formData);
  }

  if (result.success) {
    uiStore.addToast({
      message: `Category ${selectedCategory.value ? 'updated' : 'created'} successfully`,
      type: 'success'
    });
    callback(null);
  } else {
    callback(result.error);
  }
}

function confirmDelete(cat) {
  categoryToDelete.value = cat;
  isConfirmOpen.value = true;
}

async function executeDelete() {
  if (!categoryToDelete.value) return;
  isDeleting.value = true;
  const result = await categoryStore.deleteCategory(categoryToDelete.value.id);
  isDeleting.value = false;
  isConfirmOpen.value = false;

  if (result.success) {
    uiStore.addToast({
      message: 'Category deleted successfully',
      type: 'success'
    });
  } else {
    uiStore.addToast({
      message: result.error,
      type: 'error'
    });
  }
}

onMounted(() => {
  categoryStore.fetchCategories();
});
</script>

<style scoped>
.categories-page {
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

.tabs-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.tab-btn {
  padding: 0.75rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-muted);
  border-bottom: 2px solid transparent;
  transition: var(--transition);
}

.tab-btn:hover {
  color: var(--text-main);
}

.tab-btn.active {
  color: var(--primary-600);
  border-bottom-color: var(--primary-600);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}

.category-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
}

.category-main {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.category-icon-box {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 800;
  font-size: 1.15rem;
}

.category-info {
  display: flex;
  flex-direction: column;
}

.cat-title-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.cat-name {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-main);
}

.badge-default {
  font-size: 0.65rem;
  font-weight: 800;
  background: var(--bg-surface-hover);
  color: var(--text-muted);
  padding: 0.1rem 0.35rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}

.cat-meta {
  font-size: 0.775rem;
  color: var(--text-muted);
}

.category-actions {
  display: flex;
  gap: 0.25rem;
}

.delete-btn:hover {
  color: var(--expense-500);
}
</style>
