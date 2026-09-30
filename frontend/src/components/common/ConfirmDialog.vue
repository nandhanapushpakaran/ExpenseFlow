<template>
  <Modal :is-open="isOpen" :title="title" width="440px" @close="cancel">
    <div class="confirm-body">
      <div class="confirm-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>
          <line x1="12" y1="9" x2="12" y2="13"></line>
          <line x1="12" y1="17" x2="12.01" y2="17"></line>
        </svg>
      </div>
      <p class="confirm-message">{{ message }}</p>
    </div>

    <template #footer>
      <button class="btn btn-secondary" @click="cancel">Cancel</button>
      <button class="btn btn-danger" :disabled="isLoading" @click="confirm">
        <span v-if="isLoading">Processing...</span>
        <span v-else>{{ confirmText }}</span>
      </button>
    </template>
  </Modal>
</template>

<script setup>
import Modal from './Modal.vue';

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed? This action cannot be undone.'
  },
  confirmText: {
    type: String,
    default: 'Delete'
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['confirm', 'cancel']);

function confirm() {
  emit('confirm');
}

function cancel() {
  emit('cancel');
}
</script>

<style scoped>
.confirm-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  padding: 0.5rem 0;
}

.confirm-icon {
  width: 54px;
  height: 54px;
  border-radius: var(--radius-full);
  background: var(--expense-50);
  color: var(--expense-500);
  display: flex;
  align-items: center;
  justify-content: center;
}

.confirm-message {
  font-size: 0.95rem;
  color: var(--text-muted);
  line-height: 1.5;
}
</style>
