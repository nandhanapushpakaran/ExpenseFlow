<template>
  <div class="chart-container">
    <div v-if="!hasData" class="empty-state">
      <p>No expense categories to show</p>
    </div>
    <Doughnut v-else :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Doughnut } from 'vue-chartjs';
import { useAuthStore } from '@/stores/auth';
import { formatCurrency, formatPercentage } from '@/utils/formatters';

ChartJS.register(ArcElement, Title, Tooltip, Legend);

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  }
});

const authStore = useAuthStore();

const hasData = computed(() => {
  return props.categories && props.categories.length > 0;
});

const defaultColors = [
  '#6366f1', '#ec4899', '#f59e0b', '#10b981', '#06b6d4',
  '#8b5cf6', '#f97316', '#14b8a6', '#84cc16', '#e11d48'
];

const chartData = computed(() => {
  const labels = props.categories.map((c) => c.name);
  const values = props.categories.map((c) => c.total_amount || c.amount || 0);
  const colors = props.categories.map((c, idx) => c.color || defaultColors[idx % defaultColors.length]);

  return {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: colors,
        borderWidth: 2,
        borderColor: 'var(--bg-surface)'
      }
    ]
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        font: { family: 'Plus Jakarta Sans', size: 11, weight: '500' },
        usePointStyle: true,
        boxWidth: 8
      }
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          const value = context.raw;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const pct = total > 0 ? (value / total) * 100 : 0;
          return `${context.label}: ${formatCurrency(value, authStore.userCurrency)} (${formatPercentage(pct)})`;
        }
      }
    }
  },
  cutout: '70%'
}));
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 280px;
}
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);
  font-size: 0.9rem;
}
</style>
