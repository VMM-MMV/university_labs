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
        @click="loadMangaList(currentPage)" 
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

    <!-- Pagination Controls -->
    <div v-if="!isLoading && !error && filteredMangaList.length > 0" class="mt-12 flex justify-center">
      <div class="flex items-center space-x-2">
        <!-- Previous Page Button -->
        <button 
          @click="prevPage" 
          :disabled="currentPage <= 1"
          class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span class="sr-only">Previous Page</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <!-- Page Numbers -->
        <div class="flex space-x-1">
          <template v-for="page in displayedPages" :key="page">
            <button 
              v-if="page !== '...'"
              @click="goToPage(page)"
              :class="[ 
                'px-3 py-1 rounded-md transition-colors',
                currentPage === page ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'
              ]"
            >
              {{ page }}
            </button>
            <span v-else class="px-2 py-1">{{ page }}</span>
          </template>
        </div>
        
        <!-- Next Page Button -->
        <button 
          @click="nextPage" 
          :disabled="currentPage >= totalPages"
          class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span class="sr-only">Next Page</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import MangaCard from '../components/MangaCard.vue';
import FilterBar from '../components/FilterBar.vue';
import EmptyState from '../components/EmptyState.vue';
import { useRestStore } from '../composables/useRestStore';
import { useFavorites } from '../composables/useFavorites';

const route = useRoute();
const router = useRouter();

const { mangaList, isLoading, error, allGenres, loadMangaList, paginationInfo } = useRestStore();
const { isFavorite, toggleFavorite } = useFavorites();

// Filter state
const searchQuery = ref('');
const selectedGenre = ref('');
const sortBy = ref('title');

// Pagination state
const currentPage = ref(parseInt(route.query.page) || 1);
const totalPages = computed(() => mangaList.totalPage);

// Load initial page
onMounted(() => {
  loadMangaList(currentPage.value);
});

// Keep query param in sync with page
watch(currentPage, (newPage) => {
  router.replace({ query: { ...route.query, page: newPage } });
});

let hasMounted = false;

watch([searchQuery, selectedGenre], () => {
  if (hasMounted) {
    currentPage.value = 1;
    loadMangaList(1);
  }
});

onMounted(() => {
  hasMounted = true;
});

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  selectedGenre.value = '';
  sortBy.value = 'title';
  // currentPage.value = 1;
  loadMangaList(1);
};

// Filter and sort manga list
const filteredMangaList = computed(() => {
  let filtered = [...mangaList.value];
  
  if (searchQuery.value.trim() !== '') {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(manga =>
      manga.title?.toLowerCase().includes(query) ||
      manga.description?.toLowerCase().includes(query)
    );
  }

  if (selectedGenre.value) {
    filtered = filtered.filter(manga =>
      manga.genres && manga.genres.includes(selectedGenre.value)
    );
  }

  return filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'title': return a.title.localeCompare(b.title);
      case 'titleDesc': return b.title.localeCompare(a.title);
      default: return 0;
    }
  });
});

// Pagination logic
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadMangaList(currentPage.value);
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    loadMangaList(currentPage.value);
  }
};

const goToPage = (page) => {
  if (page !== currentPage.value) {
    currentPage.value = page;
    loadMangaList(page);
  }
};

const displayedPages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  const pages = [];

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    pages.push(1);

    if (current <= 3) {
      pages.push(2, 3, 4, 5, '...', total);
    } else if (current >= total - 2) {
      pages.push('...', total - 3, total - 2, total - 1, total);
    } else {
      pages.push('...', current - 1, current, current + 1, '...', total);
    }
  }

  return pages;
});

// Reset to page 1 on filter change
watch([searchQuery, selectedGenre], () => {
  currentPage.value = 1;
  loadMangaList(1);
});

</script>
