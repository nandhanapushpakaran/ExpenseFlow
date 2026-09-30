<template>
  <div class="card auth-card">
    <div class="auth-header">
      <h2 class="auth-title">Create Account</h2>
      <p class="auth-subtitle">Start managing your personal finances today</p>
    </div>

    <AlertMessage v-if="authStore.error" :message="authStore.error" type="error" />
    <AlertMessage v-if="validationError" :message="validationError" type="error" />

    <form @submit.prevent="handleRegister" class="auth-form">
      <div class="form-group">
        <label class="form-label" for="name">Full Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          placeholder="Alex Johnson"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label" for="email">Email Address</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="alex@example.com"
          required
        />
      </div>

      <div class="form-group">
        <label class="form-label" for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="At least 6 characters"
          required
          minlength="6"
        />
      </div>

      <div class="form-group">
        <label class="form-label" for="currency">Preferred Currency</label>
        <select id="currency" v-model="currency">
          <option value="USD">USD ($) - US Dollar</option>
          <option value="EUR">EUR (€) - Euro</option>
          <option value="GBP">GBP (£) - British Pound</option>
          <option value="CAD">CAD (CA$) - Canadian Dollar</option>
          <option value="AUD">AUD (A$) - Australian Dollar</option>
          <option value="INR">INR (₹) - Indian Rupee</option>
          <option value="JPY">JPY (¥) - Japanese Yen</option>
        </select>
      </div>

      <button
        type="submit"
        class="btn btn-primary btn-submit"
        :disabled="authStore.isLoading"
      >
        <span v-if="authStore.isLoading">Creating account...</span>
        <span v-else>Register & Get Started</span>
      </button>
    </form>

    <div class="auth-switch">
      <span>Already have an account? </span>
      <router-link to="/login">Sign in</router-link>
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

const name = ref('');
const email = ref('');
const password = ref('');
const currency = ref('USD');
const validationError = ref('');

async function handleRegister() {
  validationError.value = '';
  if (password.value.length < 6) {
    validationError.value = 'Password must be at least 6 characters long';
    return;
  }

  const result = await authStore.register({
    name: name.value.trim(),
    email: email.value.trim(),
    password: password.value,
    preferred_currency: currency.value
  });

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
