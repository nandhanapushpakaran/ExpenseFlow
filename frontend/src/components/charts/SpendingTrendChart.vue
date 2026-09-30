<template>
  <div class="chart-container">
    <div v-if="!hasData" class="empty-state">
      <p>No trend data available</p>
    </div>
    <Line v-else :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  CategoryScale,
  LinearScale,
  Filler
} from 'chart.js';
import { Line } from 'vue-chartjs';
import { useAuthStore } from '@/stores/auth';
import { formatCurrency } from '@/utils/formatters';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const props = defineProps({
  trendData: {
    type: Array,
    default: () => []
  }
});

const authStore = useAuthStore();

const hasData = computed(() => props.trendData && props.trendData.length > 0);

const chartData = computed(() => {
  const labels = props.trendData.map((d) => d.date || d.label);
  const values = props.trendData.map((d) => d.amount || 0);

  return {
    labels,
    datasets: [
      {
        label: 'Expenses',
        data: values,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        tension: 0.35,
        fill: true,
        pointBackgroundColor: '#6366f1',
        pointRadius: 4,
        pointHoverRadius: 6
      }
    ]
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: function (context) {
          return `Expenses: ${formatCurrency(context.raw, authStore.userCurrency)}`;
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
