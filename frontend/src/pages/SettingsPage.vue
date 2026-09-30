<template>
  <div class="settings-page">
    <div class="page-header">
      <div>
        <h2 class="page-title">Settings</h2>
        <p class="page-subtitle">Manage your profile, currency preference, and appearance</p>
      </div>
    </div>

    <div class="settings-grid">
      <!-- Profile & Preferences Card -->
      <div class="card settings-card">
        <h3 class="card-title">User Profile</h3>
        <p class="card-desc">Update your personal information and default currency</p>

        <AlertMessage v-if="successMsg" :message="successMsg" type="success" dismissible @dismiss="successMsg = ''" />
        <AlertMessage v-if="errorMsg" :message="errorMsg" type="error" dismissible @dismiss="errorMsg = ''" />

        <form @submit.prevent="handleUpdateProfile">
          <div class="form-group">
            <label class="form-label" for="profile_name">Full Name</label>
            <input
              id="profile_name"
              v-model="name"
              type="text"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="profile_email">Email Address</label>
            <input
              id="profile_email"
              :value="authStore.user?.email"
              type="email"
              disabled
              class="disabled-input"
            />
            <span class="field-hint">Email address is permanently linked to your account</span>
          </div>

          <div class="form-group">
            <label class="form-label" for="profile_currency">Preferred Currency</label>
            <select id="profile_currency" v-model="currency">
              <option value="USD">USD ($) - US Dollar</option>
              <option value="EUR">EUR (€) - Euro</option>
              <option value="GBP">GBP (£) - British Pound</option>
              <option value="CAD">CAD (CA$) - Canadian Dollar</option>
              <option value="AUD">AUD (A$) - Australian Dollar</option>
              <option value="INR">INR (₹) - Indian Rupee</option>
              <option value="JPY">JPY (¥) - Japanese Yen</option>
            </select>
            <span class="field-hint">All dashboard and transaction values will be formatted in this currency</span>
          </div>

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="authStore.isLoading"
          >
            <span v-if="authStore.isLoading">Saving...</span>
            <span v-else>Save Changes</span>
          </button>
        </form>
      </div>

      <!-- Appearance & Theme Card -->
      <div class="card settings-card">
        <h3 class="card-title">Appearance</h3>
        <p class="card-desc">Choose between light and dark visual aesthetics</p>

        <div class="theme-options">
          <div
            class="theme-choice"
            :class="{ active: uiStore.theme === 'light' }"
            @click="setTheme('light')"
          >
            <div class="theme-preview light-preview">
              <div class="preview-bar"></div>
              <div class="preview-content"></div>
            </div>
            <span class="theme-label">Light Mode</span>
          </div>

          <div
            class="theme-choice"
            :class="{ active: uiStore.theme === 'dark' }"
            @click="setTheme('dark')"
          >
            <div class="theme-preview dark-preview">
              <div class="preview-bar"></div>
              <div class="preview-content"></div>
            </div>
            <span class="theme-label">Dark Mode</span>
          </div>
        </div>

        <div class="tech-stack-box">
          <h4 class="tech-title">Portfolio Technology Stack</h4>
          <ul class="tech-list">
            <li><strong>Frontend:</strong> Vue 3, Vite, Pinia, Vue Router, Chart.js</li>
            <li><strong>Backend:</strong> FastAPI, Python 3.11, Pydantic v2</li>
            <li><strong>Database:</strong> PostgreSQL, SQLAlchemy 2.0, Alembic</li>
            <li><strong>Security:</strong> JWT tokens, Bcrypt password hashing</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useUiStore } from '@/stores/ui';
import AlertMessage from '@/components/common/AlertMessage.vue';

const authStore = useAuthStore();
const uiStore = useUiStore();

const name = ref(authStore.userName || '');
const currency = ref(authStore.userCurrency || 'USD');
const successMsg = ref('');
const errorMsg = ref('');

function setTheme(theme) {
  uiStore.toggleTheme();
  if (uiStore.theme !== theme) {
    uiStore.toggleTheme();
  }
}

async function handleUpdateProfile() {
  successMsg.value = '';
  errorMsg.value = '';

  const res = await authStore.updateProfile({
    name: name.value.trim(),
    preferred_currency: currency.value
  });

  if (res.success) {
    successMsg.value = 'Profile and currency preferences updated!';
    uiStore.addToast({ message: 'Settings saved successfully', type: 'success' });
  } else {
    errorMsg.value = res.error || 'Failed to update profile';
  }
}

onMounted(() => {
  if (authStore.user) {
    name.value = authStore.user.name;
    currency.value = authStore.user.preferred_currency || 'USD';
  }
});
</script>

<style scoped>
.settings-page {
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.925rem;
  color: var(--text-muted);
  margin-top: 0.2rem;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.settings-card {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-main);
}

.card-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.disabled-input {
  opacity: 0.65;
  background-color: var(--bg-app);
  cursor: not-allowed;
}

.field-hint {
  font-size: 0.775rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

.theme-options {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.theme-choice {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  padding: 0.75rem;
  border-radius: var(--radius-lg);
  border: 2px solid var(--border-color);
  transition: var(--transition);
}

.theme-choice:hover {
  border-color: var(--primary-400);
}

.theme-choice.active {
  border-color: var(--primary-600);
  background: var(--primary-50);
}

[data-theme='dark'] .theme-choice.active {
  background: rgba(99, 102, 241, 0.12);
}

.theme-preview {
  width: 100%;
  height: 70px;
  border-radius: var(--radius-md);
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.light-preview {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.light-preview .preview-bar {
  height: 12px;
  background: #6366f1;
  border-radius: 3px;
  width: 50%;
}

.light-preview .preview-content {
  flex: 1;
  background: #ffffff;
  border-radius: 4px;
}

.dark-preview {
  background: #0b0f19;
  border: 1px solid #1e293b;
}

.dark-preview .preview-bar {
  height: 12px;
  background: #818cf8;
  border-radius: 3px;
  width: 50%;
}

.dark-preview .preview-content {
  flex: 1;
  background: #131b2e;
  border-radius: 4px;
}

.theme-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-main);
}

.tech-stack-box {
  background: var(--bg-app);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 1.25rem;
}

.tech-title {
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--text-main);
}

.tech-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

@media (max-width: 900px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
