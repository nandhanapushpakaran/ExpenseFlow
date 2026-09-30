<template>
  <div class="card filters-card">
    <div class="filters-grid">
      <!-- Search Input -->
      <div class="filter-item search-filter">
        <label class="filter-label">Search</label>
        <div class="search-input-wrapper">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search description..."
            @input="handleSearchInput"
          />
        </div>
      </div>

      <!-- Type Filter -->
      <div class="filter-item">
        <label class="filter-label">Type</label>
        <select v-model="selectedType" @change="applyFilters">
          <option value="">All Types</option>
          <option value="INCOME">Income Only</option>
          <option value="EXPENSE">Expense Only</option>
        </select>
      </div>

      <!-- Category Filter -->
      <div class="filter-item">
        <label class="filter-label">Category</label>
        <select v-model="selectedCategory" @change="applyFilters">
          <option value="">All Categories</option>
          <option
            v-for="cat in filteredCategories"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.name }} ({{ cat.type }})
          </option>
        </select>
      </div>

      <!-- Date Range: Start Date -->
      <div class="filter-item">
        <label class="filter-label">From Date</label>
        <input
          v-model="startDate"
          type="date"
          @change="applyFilters"
        />
      </div>

      <!-- Date Range: End Date -->
      <div class="filter-item">
        <label class="filter-label">To Date</label>
        <input
          v-model="endDate"
          type="date"
          @change="applyFilters"
        />
      </div>

      <!-- Filter Actions -->
      <div class="filter-actions">
        <button
          class="btn btn-secondary btn-sm"
          title="Clear all filters"
          @click="resetFilters"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="1 4 1 10 7 10"></polyline>
            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
          </svg>
          <span>Reset</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCategoryStore } from '@/stores/categories';

const props = defineProps({
  filters: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update-filters', 'reset-filters']);

const categoryStore = useCategoryStore();

const searchQuery = ref(props.filters.search || '');
const selectedType = ref(props.filters.type || '');
const selectedCategory = ref(props.filters.category_id || '');
const startDate = ref(props.filters.start_date || '');
const endDate = ref(props.filters.end_date || '');

let searchDebounceTimer = null;

const filteredCategories = computed(() => {
  if (!selectedType.value) return categoryStore.categories;
  return categoryStore.categories.filter((c) => c.type === selectedType.value);
});

function handleSearchInput() {
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    applyFilters();
  }, 350);
}

function applyFilters() {
  emit('update-filters', {
    search: searchQuery.value.trim(),
    type: selectedType.value,
    category_id: selectedCategory.value,
    start_date: startDate.value,
    end_date: endDate.value
  });
}

function resetFilters() {
  searchQuery.value = '';
  selectedType.value = '';
  selectedCategory.value = '';
  startDate.value = '';
  endDate.value = '';
  emit('reset-filters');
}
</script>

<style scoped>
.filters-card {
  padding: 1.15rem 1.25rem;
  margin-bottom: 1.5rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1.2fr 1fr 1fr auto;
  gap: 0.85rem;
  align-items: flex-end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.filter-label {
  font-size: 0.775rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  color: var(--text-subtle);
  pointer-events: none;
}

.search-input-wrapper input {
  padding-left: 2.2rem;
}

.filter-actions {
  display: flex;
  align-items: center;
}

@media (max-width: 1024px) {
  .filters-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .filters-grid {
    grid-template-columns: 1fr;
  }
}
</style>
