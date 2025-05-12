<template>
  <span 
    class="px-2 py-1 text-base-100 rounded transition-colors"
    :class="[
      interactive ? 'cursor-pointer' : '',
      isActive ? 'bg-blue-500 text-white' : 'bg-accent hover:bg-accent'
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