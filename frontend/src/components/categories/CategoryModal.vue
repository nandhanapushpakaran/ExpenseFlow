<template>
  <Modal
    :is-open="isOpen"
    :title="isEditing ? 'Edit Category' : 'Create Category'"
    width="480px"
    @close="handleClose"
  >
    <form @submit.prevent="handleSubmit">
      <AlertMessage v-if="serverError" :message="serverError" type="error" />

      <!-- Category Type -->
      <div class="form-group">
        <label class="form-label">Category Type *</label>
        <div class="type-selector">
          <button
            type="button"
            class="type-pill"
            :class="{ active: form.type === 'EXPENSE' }"
            @click="form.type = 'EXPENSE'"
          >
            Expense
          </button>
          <button
            type="button"
            class="type-pill"
            :class="{ active: form.type === 'INCOME' }"
            @click="form.type = 'INCOME'"
          >
            Income
          </button>
        </div>
      </div>

      <!-- Category Name -->
      <div class="form-group">
        <label class="form-label" for="category_name">Category Name *</label>
        <input
          id="category_name"
          v-model="form.name"
          type="text"
          placeholder="e.g., Subscriptions, Pet Care, Bonuses"
          required
          maxlength="50"
        />
        <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
      </div>

      <!-- Color Palette -->
      <div class="form-group">
        <label class="form-label">Category Color</label>
        <div class="color-palette">
          <button
            v-for="color in presetColors"
            :key="color"
            type="button"
            class="color-swatch"
            :style="{ backgroundColor: color }"
            :class="{ selected: form.color === color }"
            @click="form.color = color"
          >
            <svg v-if="form.color === color" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </button>
        </div>
      </div>

      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="handleClose">Cancel</button>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          <span v-if="isSubmitting">Saving...</span>
          <span v-else>{{ isEditing ? 'Update Category' : 'Create Category' }}</span>
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Modal from '@/components/common/Modal.vue';
import AlertMessage from '@/components/common/AlertMessage.vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  category: {
    type: Object,
    default: null
  },
  defaultType: {
    type: String,
    default: 'EXPENSE'
  }
});

const emit = defineEmits(['close', 'submit']);

const isEditing = computed(() => !!props.category?.id);
const isSubmitting = ref(false);
const serverError = ref('');
const errors = ref({});

const presetColors = [
  '#6366f1', '#3b82f6', '#0ea5e9', '#06b6d4', '#10b981',
  '#84cc16', '#eab308', '#f97316', '#f43f5e', '#ec4899',
  '#a855f7', '#64748b'
];

const form = ref({
  name: '',
  type: props.defaultType,
  color: presetColors[0]
});

watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      serverError.value = '';
      errors.value = {};
      if (props.category) {
        form.value = {
          name: props.category.name,
          type: props.category.type,
          color: props.category.color || presetColors[0]
        };
      } else {
        form.value = {
          name: '',
          type: props.defaultType || 'EXPENSE',
          color: presetColors[0]
        };
      }
    }
  }
);

function validate() {
  const errs = {};
  if (!form.value.name || !form.value.name.trim()) {
    errs.name = 'Category name is required';
  }
  errors.value = errs;
  return Object.keys(errs).length === 0;
}

function handleSubmit() {
  if (!validate()) return;
  isSubmitting.value = true;
  serverError.value = '';

  emit('submit', { ...form.value, name: form.value.name.trim() }, (errorMessage) => {
    isSubmitting.value = false;
    if (errorMessage) {
      serverError.value = errorMessage;
    } else {
      handleClose();
    }
  });
}

function handleClose() {
  emit('close');
}
</script>

<style scoped>
.type-selector {
  display: flex;
  gap: 0.5rem;
}

.type-pill {
  flex: 1;
  padding: 0.55rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg-surface);
  transition: var(--transition);
}

.type-pill.active {
  border-color: var(--primary-500);
  background: var(--primary-50);
  color: var(--primary-600);
}

.color-palette {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.color-swatch {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.color-swatch:hover {
  transform: scale(1.15);
}

.color-swatch.selected {
  outline: 3px solid var(--border-focus);
  outline-offset: 2px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}
</style>
