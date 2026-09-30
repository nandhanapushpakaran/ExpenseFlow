<template>
  <Modal
    :is-open="isOpen"
    :title="isEditing ? 'Edit Transaction' : 'Add New Transaction'"
    width="540px"
    @close="handleClose"
  >
    <form @submit.prevent="handleSubmit">
      <AlertMessage v-if="serverError" :message="serverError" type="error" />

      <!-- Transaction Type Switcher -->
      <div class="type-toggle-container">
        <button
          type="button"
          class="type-btn"
          :class="{ 'active-expense': form.type === 'EXPENSE' }"
          @click="setType('EXPENSE')"
        >
          Expense
        </button>
        <button
          type="button"
          class="type-btn"
          :class="{ 'active-income': form.type === 'INCOME' }"
          @click="setType('INCOME')"
        >
          Income
        </button>
      </div>

      <!-- Amount Field -->
      <div class="form-group">
        <label class="form-label" for="amount">Amount ({{ authStore.userCurrency }}) *</label>
        <div class="input-with-symbol">
          <input
            id="amount"
            v-model.number="form.amount"
            type="number"
            step="0.01"
            min="0.01"
            placeholder="0.00"
            required
            class="font-mono"
            :class="{ 'is-invalid': errors.amount }"
          />
        </div>
        <span v-if="errors.amount" class="form-error">{{ errors.amount }}</span>
      </div>

      <!-- Category Selection -->
      <div class="form-group">
        <label class="form-label" for="category_id">Category *</label>
        <select
          id="category_id"
          v-model="form.category_id"
          required
          :class="{ 'is-invalid': errors.category_id }"
        >
          <option value="" disabled>Select a category</option>
          <option
            v-for="cat in availableCategories"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.name }}
          </option>
        </select>
        <span v-if="errors.category_id" class="form-error">{{ errors.category_id }}</span>
      </div>

      <!-- Date and Payment Method in Grid -->
      <div class="form-row">
        <div class="form-group">
          <label class="form-label" for="transaction_date">Date *</label>
          <input
            id="transaction_date"
            v-model="form.transaction_date"
            type="date"
            required
            :class="{ 'is-invalid': errors.transaction_date }"
          />
          <span v-if="errors.transaction_date" class="form-error">{{ errors.transaction_date }}</span>
        </div>

        <div class="form-group">
          <label class="form-label" for="payment_method">Payment Method</label>
          <select id="payment_method" v-model="form.payment_method">
            <option value="Debit Card">Debit Card</option>
            <option value="Credit Card">Credit Card</option>
            <option value="Cash">Cash</option>
            <option value="Bank Transfer">Bank Transfer</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>

      <!-- Description -->
      <div class="form-group">
        <label class="form-label" for="description">Description *</label>
        <input
          id="description"
          v-model="form.description"
          type="text"
          placeholder="e.g., Grocery shopping at Trader Joe's"
          required
          maxlength="255"
          :class="{ 'is-invalid': errors.description }"
        />
        <span v-if="errors.description" class="form-error">{{ errors.description }}</span>
      </div>

      <!-- Optional Notes -->
      <div class="form-group">
        <label class="form-label" for="notes">Notes (Optional)</label>
        <textarea
          id="notes"
          v-model="form.notes"
          rows="3"
          placeholder="Additional details, receipts or tags..."
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="handleClose">Cancel</button>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          <span v-if="isSubmitting">Saving...</span>
          <span v-else>{{ isEditing ? 'Update Transaction' : 'Save Transaction' }}</span>
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Modal from '@/components/common/Modal.vue';
import AlertMessage from '@/components/common/AlertMessage.vue';
import { useAuthStore } from '@/stores/auth';
import { useCategoryStore } from '@/stores/categories';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  transaction: {
    type: Object,
    default: null
  },
  defaultType: {
    type: String,
    default: 'EXPENSE'
  }
});

const emit = defineEmits(['close', 'submit']);

const authStore = useAuthStore();
const categoryStore = useCategoryStore();

const isEditing = computed(() => !!props.transaction?.id);
const isSubmitting = ref(false);
const serverError = ref('');
const errors = ref({});

const getTodayString = () => new Date().toISOString().split('T')[0];

const form = ref({
  type: props.defaultType,
  amount: '',
  category_id: '',
  transaction_date: getTodayString(),
  description: '',
  notes: '',
  payment_method: 'Debit Card'
});

const availableCategories = computed(() => {
  return form.value.type === 'INCOME'
    ? categoryStore.incomeCategories
    : categoryStore.expenseCategories;
});

function setType(type) {
  form.value.type = type;
  // If current category is not in the new type list, reset category
  const validCategory = availableCategories.value.some((c) => c.id === form.value.category_id);
  if (!validCategory) {
    form.value.category_id = availableCategories.value[0]?.id || '';
  }
}

watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      serverError.value = '';
      errors.value = {};
      if (props.transaction) {
        form.value = {
          type: props.transaction.type,
          amount: props.transaction.amount,
          category_id: props.transaction.category_id,
          transaction_date: props.transaction.transaction_date?.slice(0, 10) || getTodayString(),
          description: props.transaction.description,
          notes: props.transaction.notes || '',
          payment_method: props.transaction.payment_method || 'Debit Card'
        };
      } else {
        form.value = {
          type: props.defaultType || 'EXPENSE',
          amount: '',
          category_id: '',
          transaction_date: getTodayString(),
          description: '',
          notes: '',
          payment_method: 'Debit Card'
        };
        // Auto-select first matching category
        if (availableCategories.value.length > 0) {
          form.value.category_id = availableCategories.value[0].id;
        }
      }
    }
  }
);

function validate() {
  const errs = {};
  if (!form.value.amount || Number(form.value.amount) <= 0) {
    errs.amount = 'Amount must be greater than 0';
  }
  if (!form.value.category_id) {
    errs.category_id = 'Please choose a category';
  }
  if (!form.value.transaction_date) {
    errs.transaction_date = 'Date is required';
  }
  if (!form.value.description || !form.value.description.trim()) {
    errs.description = 'Description is required';
  }
  errors.value = errs;
  return Object.keys(errs).length === 0;
}

async function handleSubmit() {
  if (!validate()) return;
  isSubmitting.value = true;
  serverError.value = '';

  const payload = {
    ...form.value,
    amount: parseFloat(form.value.amount)
  };

  try {
    emit('submit', payload, (errorMessage) => {
      isSubmitting.value = false;
      if (errorMessage) {
        serverError.value = errorMessage;
      } else {
        handleClose();
      }
    });
  } catch (err) {
    isSubmitting.value = false;
    serverError.value = err.message || 'An error occurred';
  }
}

function handleClose() {
  emit('close');
}
</script>

<style scoped>
.type-toggle-container {
  display: flex;
  background: var(--bg-app);
  border-radius: var(--radius-md);
  padding: 0.25rem;
  margin-bottom: 1.25rem;
  border: 1px solid var(--border-color);
}

.type-btn {
  flex: 1;
  padding: 0.6rem;
  font-size: 0.9rem;
  font-weight: 700;
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  transition: var(--transition);
}

.type-btn.active-expense {
  background: var(--expense-500);
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(244, 63, 94, 0.3);
}

.type-btn.active-income {
  background: var(--income-500);
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.is-invalid {
  border-color: var(--expense-500) !important;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>
