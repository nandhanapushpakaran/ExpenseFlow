<template>
  <div v-if="message" class="alert" :class="[`alert-${type}`]">
    <div class="alert-icon">
      <svg v-if="type === 'error'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="15" y1="9" x2="9" y2="15"></line>
        <line x1="9" y1="9" x2="15" y2="15"></line>
      </svg>
      <svg v-else-if="type === 'success'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
    </div>
    <div class="alert-text">{{ message }}</div>
    <button v-if="dismissible" class="alert-dismiss" @click="$emit('dismiss')">×</button>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'error' // 'error' | 'success' | 'warning' | 'info'
  },
  dismissible: {
    type: Boolean,
    default: false
  }
});

defineEmits(['dismiss']);
</script>

<style scoped>
.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1.15rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1.25rem;
}

.alert-error {
  background-color: var(--expense-50);
  color: var(--expense-600);
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.alert-success {
  background-color: var(--income-50);
  color: var(--income-600);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.alert-warning {
  background-color: var(--warning-50);
  color: var(--warning-600);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.alert-info {
  background-color: var(--info-50);
  color: var(--info-500);
  border: 1px solid rgba(14, 165, 233, 0.3);
}

.alert-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.alert-text {
  flex: 1;
}

.alert-dismiss {
  font-size: 1.25rem;
  line-height: 1;
  color: inherit;
  opacity: 0.7;
}

.alert-dismiss:hover {
  opacity: 1;
}
</style>
