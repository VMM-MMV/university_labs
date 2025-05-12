<template>
  <div class="mb-8 bg-base-300 text-secondary p-4 rounded-lg shadow">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Search Bar -->
      <div class="md:col-span-1">
        <label for="search" class="block text-sm font-medium mb-1">Search</label>
        <input
          type="text"
          id="search"
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
          placeholder="Search manga titles..."
          class="w-full h-9.5 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <!-- Genre Filter -->
      <div class="md:col-span-1">
        <label for="genre" class="block text-sm font-medium mb-1">Genre</label>
        <select
          id="genre"
          :value="selectedGenre"
          @change="$emit('update:selectedGenre', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Genres</option>
          <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
        </select>
      </div>
      
      <!-- Sort By -->
      <div class="md:col-span-1">
        <label for="sortBy" class="block text-sm font-medium mb-1">Sort By</label>
        <select
          id="sortBy"
          :value="sortBy"
          @change="$emit('update:sortBy', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="title">Title (A-Z)</option>
          <option value="titleDesc">Title (Z-A)</option>
          <!-- Add more sorting options as needed -->
        </select>
      </div>
    </div>
    
    <!-- Active Filters -->
    <div class="mt-4 flex flex-wrap items-center gap-2" v-if="selectedGenre">
      <span class="text-sm text-gray-700">Active filters:</span>
      <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center">
        {{ selectedGenre }}
        <button @click="$emit('update:selectedGenre', '')" class="ml-1 focus:outline-none">
          <span class="text-xs font-bold">×</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  searchQuery: {
    type: String,
    required: true
  },
  selectedGenre: {
    type: String,
    required: true
  },
  sortBy: {
    type: String,
    required: true
  },
  genres: {
    type: Array,
    required: true
  }
});

defineEmits(['update:searchQuery', 'update:selectedGenre', 'update:sortBy', 'resetFilters']);
</script>