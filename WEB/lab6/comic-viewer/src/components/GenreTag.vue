<template>
  <span 
    class="px-2 py-1 text-xs rounded transition-colors"
    :class="[
      interactive ? 'cursor-pointer' : '',
      isActive ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'
    ]"
    @click="interactive && onClick()"
  >
    {{ genre }}
  </span>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  genre: {
    type: String,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  },
  interactive: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['click']);

const onClick = () => {
  emit('click', props.genre);
};
</script>