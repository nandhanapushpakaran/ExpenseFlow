import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { setActivePinia, createPinia } from 'pinia';
import TransactionForm from '@/components/transactions/TransactionForm.vue';
import { useCategoryStore } from '@/stores/categories';

describe('TransactionForm Component', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const categoryStore = useCategoryStore();
    categoryStore.categories = [
      { id: 1, name: 'Salary', type: 'INCOME', color: '#10b981', is_default: true },
      { id: 2, name: 'Groceries', type: 'EXPENSE', color: '#f43f5e', is_default: true }
    ];
  });

  it('renders correctly when open', () => {
    const wrapper = mount(TransactionForm, {
      props: {
        isOpen: true,
        defaultType: 'EXPENSE'
      },
      global: {
        stubs: {
          Teleport: true
        }
      }
    });

    expect(wrapper.text()).toContain('Add New Transaction');
    expect(wrapper.find('input#amount').exists()).toBe(true);
    expect(wrapper.find('select#category_id').exists()).toBe(true);
    expect(wrapper.find('input#description').exists()).toBe(true);
  });

  it('shows validation errors when submitting empty form', async () => {
    const wrapper = mount(TransactionForm, {
      props: {
        isOpen: true
      },
      global: {
        stubs: {
          Teleport: true
        }
      }
    });

    await wrapper.find('form').trigger('submit.prevent');

    // Should show validation error for amount
    expect(wrapper.text()).toContain('Amount must be greater than 0');
  });
});
