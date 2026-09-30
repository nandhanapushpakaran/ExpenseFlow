<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue';
import { useUiStore } from '@/stores/ui';
import { useAuthStore } from '@/stores/auth';

const uiStore = useUiStore();
const authStore = useAuthStore();

onMounted(async () => {
  uiStore.initTheme();
  if (authStore.token) {
    await authStore.fetchCurrentUser();
  }
});
</script>

<style>
/* Base root styles */
</style>
