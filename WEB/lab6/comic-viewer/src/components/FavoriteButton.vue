<template>
  <button 
    @click.prevent="$emit('toggle')"
    class="absolute top-2 right-2 bg-white rounded-full p-2 shadow hover:bg-gray-100 z-8"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="isFavorite ? 'text-red-500' : 'text-gray-400'" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
    </svg>
  </button>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  isFavorite: {
    type: Boolean,
    required: true
  }
});

defineEmits(['toggle']);
</script>