<template>
  <div class="card stat-card" :class="[`stat-${variant}`]">
    <div class="stat-header">
      <span class="stat-title">{{ title }}</span>
      <div class="stat-icon-wrapper" :class="[`icon-${variant}`]">
        <slot name="icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
          </svg>
        </slot>
      </div>
    </div>

    <div class="stat-body">
      <div class="stat-value font-mono">{{ formattedValue }}</div>
      <div v-if="changePct !== null && changePct !== undefined" class="stat-trend">
        <span
          class="trend-badge"
          :class="{
            'trend-positive': changePct > 0,
            'trend-negative': changePct < 0,
            'trend-neutral': changePct === 0
          }"
        >
          <span v-if="changePct > 0">↑</span>
          <span v-else-if="changePct < 0">↓</span>
          <span>{{ Math.abs(changePct).toFixed(1) }}%</span>
        </span>
        <span class="stat-subtext">{{ subtext || 'vs last month' }}</span>
      </div>
      <div v-else-if="subtext" class="stat-subtext-only">
        {{ subtext }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { formatCurrency, formatPercentage } from '@/utils/formatters';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    default: 0
  },
  type: {
    type: String,
    default: 'currency' // 'currency' | 'percentage' | 'number'
  },
  variant: {
    type: String,
    default: 'primary' // 'primary' | 'income' | 'expense' | 'info'
  },
  changePct: {
    type: Number,
    default: null
  },
  subtext: {
    type: String,
    default: ''
  }
});

const authStore = useAuthStore();

const formattedValue = computed(() => {
  if (props.type === 'percentage') {
    return formatPercentage(props.value);
  }
  if (props.type === 'number') {
    return Number(props.value).toLocaleString();
  }
  return formatCurrency(props.value, authStore.userCurrency);
});
</script>

<style scoped>
.stat-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.stat-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.stat-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-primary {
  background: var(--primary-50);
  color: var(--primary-600);
}

.icon-income {
  background: var(--income-50);
  color: var(--income-600);
}

.icon-expense {
  background: var(--expense-50);
  color: var(--expense-600);
}

.icon-info {
  background: var(--info-50);
  color: var(--info-500);
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.trend-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-sm);
}

.trend-positive {
  background: var(--income-50);
  color: var(--income-600);
}

.trend-negative {
  background: var(--expense-50);
  color: var(--expense-600);
}

.trend-neutral {
  background: var(--bg-surface-hover);
  color: var(--text-muted);
}

.stat-subtext, .stat-subtext-only {
  font-size: 0.775rem;
  color: var(--text-muted);
}

.stat-subtext-only {
  margin-top: 0.5rem;
}
</style>
