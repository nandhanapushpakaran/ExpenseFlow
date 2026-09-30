import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { setActivePinia, createPinia } from 'pinia';
import StatCard from '@/components/common/StatCard.vue';

describe('StatCard Component', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renders title and formatted currency value correctly', () => {
    const wrapper = mount(StatCard, {
      props: {
        title: 'Total Income',
        value: 3500,
        variant: 'income'
      }
    });

    expect(wrapper.text()).toContain('Total Income');
    expect(wrapper.text()).toContain('3,500.00');
  });

  it('renders percentage values correctly when type="percentage"', () => {
    const wrapper = mount(StatCard, {
      props: {
        title: 'Savings Rate',
        value: 42.5,
        type: 'percentage'
      }
    });

    expect(wrapper.text()).toContain('42.5%');
  });

  it('renders positive trend badge with up arrow', () => {
    const wrapper = mount(StatCard, {
      props: {
        title: 'Income',
        value: 1000,
        changePct: 15.2
      }
    });

    expect(wrapper.find('.trend-positive').exists()).toBe(true);
    expect(wrapper.text()).toContain('15.2%');
    expect(wrapper.text()).toContain('↑');
  });
});
