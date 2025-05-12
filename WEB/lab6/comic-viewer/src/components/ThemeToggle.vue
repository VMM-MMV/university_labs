<template>
  <input
    type="checkbox"
    class="toggle theme-controller"
    :checked="theme === 'dracula'"
    @change="toggleTheme"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { watch, onMounted } from 'vue';

const theme = ref<'caramellatte' | 'dracula'>('caramellatte')

// Load stored theme or default
onMounted(() => {
  const storedTheme = localStorage.getItem('theme') as 'caramellatte' | 'dracula'
  theme.value = storedTheme || 'caramellatte'
  document.documentElement.setAttribute('data-theme', theme.value)
})

// Watch and apply theme changes
watch(theme, (newTheme) => {
  document.documentElement.setAttribute('data-theme', newTheme)
  localStorage.setItem('theme', newTheme)
})

// Toggle handler
function toggleTheme() {
  theme.value = theme.value === 'caramellatte' ? 'dracula' : 'caramellatte'
}
</script>
