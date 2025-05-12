<template>
  <div class="text-center py-12 bg-base-300 rounded-lg shadow">
    <div class="text-gray-500 text-lg mb-4">{{ message }}</div>
    <slot name="action">
      <button 
        v-if="actionText" 
        @click="$emit('action')" 
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        {{ actionText }}
      </button>
    </slot>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  message: {
    type: String,
    required: true
  },
  actionText: {
    type: String,
    default: ''
  }
});

defineEmits(['action']);
</script>