<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Filter and Search Section -->
    <FilterBar 
      v-model:searchQuery="searchQuery"
      v-model:selectedGenre="selectedGenre"
      v-model:sortBy="sortBy"
      :genres="allGenres"
    />

    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="text-gray-500 text-lg">Loading manga...</div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-lg">{{ error }}</div>
      <button 
        @click="loadMangaList" 
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        Try Again
      </button>
    </div>

    <!-- Manga Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
      <MangaCard
        v-for="manga in filteredMangaList"
        :key="manga.title"
        :manga="manga"
        :is-favorite="isFavorite(manga)"
        :active-genre="selectedGenre"
        :allow-genre-filter="true"
        @toggle-favorite="toggleFavorite(manga)"
        @select-genre="selectedGenre = $event"
      />
    </div>
    
    <!-- No results message -->
    <EmptyState 
      v-if="!isLoading && !error && filteredMangaList.length === 0"
      message="No manga found matching your filters"
      action-text="Reset Filters"
      @action="resetFilters"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import MangaCard from '../components/MangaCard.vue';
import FilterBar from '../components/FilterBar.vue';
import EmptyState from '../components/EmptyState.vue';
import { useMangaStore } from '../composables/useMangaStore';
import { useFavorites } from '../composables/useFavorites';

const { mangaList, isLoading, error, allGenres, loadMangaList } = useMangaStore();
const { isFavorite, toggleFavorite } = useFavorites();

// Filter state
const searchQuery = ref('');
const selectedGenre = ref('');
const sortBy = ref('title');

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  selectedGenre.value = '';
  sortBy.value = 'title';
};

// Filter and sort manga list
const filteredMangaList = computed(() => {
  let filtered = [...mangaList.value];
  
  // Filter by search query
  if (searchQuery.value.trim() !== '') {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(manga => 
      (manga.title?.toLowerCase().includes(query)) || 
      (manga.description?.toLowerCase().includes(query))
    );
  }
  
  // Filter by genre
  if (selectedGenre.value) {
    filtered = filtered.filter(manga => 
      manga.genres && manga.genres.includes(selectedGenre.value)
    );
  }
  
  // Sort the filtered list
  return filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'title':
        return a.title.localeCompare(b.title);
      case 'titleDesc':
        return b.title.localeCompare(a.title);
      default:
        return 0;
    }
  });
});
</script>