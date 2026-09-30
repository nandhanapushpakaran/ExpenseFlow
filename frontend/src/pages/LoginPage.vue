<template>
  <div class="card auth-card">
    <div class="auth-header">
      <h2 class="auth-title">Welcome Back</h2>
      <p class="auth-subtitle">Sign in to your Expense Tracker Dashboard</p>
    </div>

    <!-- Quick Demo Auto-Fill Banner -->
    <div class="demo-banner">
      <div class="demo-info">
        <span class="demo-badge">DEMO MODE</span>
        <span class="demo-text">Explore with pre-populated demo data</span>
      </div>
      <button type="button" class="btn btn-secondary btn-sm" @click="fillDemoCredentials">
        Auto-Fill Demo
      </button>
    </div>

    <AlertMessage v-if="authStore.error" :message="authStore.error" type="error" />

    <form @submit.prevent="handleLogin" class="auth-form">
      <div class="form-group">
        <label class="form-label" for="email">Email Address</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="name@example.com"
          required
          autocomplete="email"
        />
      </div>

      <div class="form-group">
        <div class="password-label-row">
          <label class="form-label" for="password">Password</label>
        </div>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          autocomplete="current-password"
        />
      </div>

      <button
        type="submit"
        class="btn btn-primary btn-submit"
        :disabled="authStore.isLoading"
      >
        <span v-if="authStore.isLoading">Signing in...</span>
        <span v-else>Sign In</span>
      </button>
    </form>

    <div class="auth-switch">
      <span>Don't have an account? </span>
      <router-link to="/register">Create an account</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import AlertMessage from '@/components/common/AlertMessage.vue';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');

function fillDemoCredentials() {
  email.value = 'demo@expensetracker.dev';
  password.value = 'DemoPass123!';
}

async function handleLogin() {
  const result = await authStore.login(email.value, password.value);
  if (result.success) {
    router.push('/dashboard');
  }
}
</script>

<style scoped>
.auth-card {
  width: 100%;
  max-width: 440px;
  padding: 2.25rem 2rem;
}

.auth-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.auth-subtitle {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: 0.35rem;
}

.demo-banner {
  background: var(--primary-50);
  border: 1px solid var(--primary-200);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

[data-theme='dark'] .demo-banner {
  background: rgba(99, 102, 241, 0.12);
  border-color: rgba(99, 102, 241, 0.25);
}

.demo-badge {
  font-size: 0.675rem;
  font-weight: 800;
  background: var(--primary-600);
  color: #ffffff;
  padding: 0.15rem 0.4rem;
  border-radius: var(--radius-sm);
  margin-right: 0.5rem;
}

.demo-text {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-main);
}

.auth-form {
  display: flex;
  flex-direction: column;
}

.btn-submit {
  width: 100%;
  padding: 0.8rem;
  margin-top: 0.75rem;
}

.auth-switch {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: var(--text-muted);
}

.auth-switch a {
  font-weight: 600;
}
</style>
