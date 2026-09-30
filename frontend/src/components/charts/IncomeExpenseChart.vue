<template>
  <div class="chart-container">
    <div v-if="!hasData" class="empty-state">
      <p>No transaction data available for this period</p>
    </div>
    <Bar v-else :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { Bar } from 'vue-chartjs';
import { useAuthStore } from '@/stores/auth';
import { formatCurrency } from '@/utils/formatters';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const props = defineProps({
  monthlyData: {
    type: Array,
    default: () => []
  }
});

const authStore = useAuthStore();

const hasData = computed(() => {
  return props.monthlyData && props.monthlyData.length > 0;
});

const chartData = computed(() => {
  const labels = props.monthlyData.map((d) => d.month_name || d.month);
  const incomeValues = props.monthlyData.map((d) => d.income || 0);
  const expenseValues = props.monthlyData.map((d) => d.expense || 0);

  return {
    labels,
    datasets: [
      {
        label: 'Income',
        backgroundColor: '#10b981',
        borderRadius: 6,
        data: incomeValues
      },
      {
        label: 'Expenses',
        backgroundColor: '#f43f5e',
        borderRadius: 6,
        data: expenseValues
      }
    ]
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' },
        usePointStyle: true,
        boxWidth: 8
      }
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          return `${context.dataset.label}: ${formatCurrency(context.raw, authStore.userCurrency)}`;
        }
      }
    }
  },
  scales: {
    x: {
      grid: { display: false }
    },
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(148, 163, 184, 0.1)' },
      ticks: {
        callback: function (value) {
          return formatCurrency(value, authStore.userCurrency);
        }
      }
    }
  }
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
