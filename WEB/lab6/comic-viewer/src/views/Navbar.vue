<!-- src/components/Navbar.vue -->
<template>
  <nav class="bg-neutral p-4 sticky top-0 z-10">
    <div class="container mx-auto">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-6">
          <router-link to="/" class="text-white text-lg font-medium hover:text-green-400">
            Manga Store
          </router-link>
          
          <div class="hidden md:flex space-x-6">
            <router-link to="/" class="text-gray-300 hover:text-white">
              Home
            </router-link>
            <router-link to="/favorites" class="text-gray-300 hover:text-white flex items-center">
              <span>Favorites</span>
            </router-link>
          </div>
        </div>

        <ThemeToggle />
      </div>
    </div>
  </nav>
</template>

<script setup>
import ThemeToggle from '../components/ThemeToggle.vue'
</script>
