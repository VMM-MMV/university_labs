<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Filter and Search Section -->
    <div class="mb-8 bg-white p-4 rounded-lg shadow">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Search Bar -->
        <div class="md:col-span-1">
          <label for="search" class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input
            type="text"
            id="search"
            v-model="searchQuery"
            placeholder="Search manga titles..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <!-- Genre Filter -->
        <div class="md:col-span-1">
          <label for="genre" class="block text-sm font-medium text-gray-700 mb-1">Genre</label>
          <select
            id="genre"
            v-model="selectedGenre"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Genres</option>
            <option v-for="genre in allGenres" :key="genre" :value="genre">{{ genre }}</option>
          </select>
        </div>
        
        <!-- Sort By -->
        <div class="md:col-span-1">
          <label for="sortBy" class="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select
            id="sortBy"
            v-model="sortBy"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="title">Title (A-Z)</option>
            <option value="titleDesc">Title (Z-A)</option>
          </select>
        </div>
      </div>
      
      <!-- Active Filters -->
      <div class="mt-4 flex flex-wrap items-center gap-2" v-if="selectedGenre">
        <span class="text-sm text-gray-700">Active filters:</span>
        <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center">
          {{ selectedGenre }}
          <button @click="selectedGenre = ''" class="ml-1 focus:outline-none">
            <span class="text-xs font-bold">×</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Manga Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
      <div
        v-for="manga in filteredMangaList"
        :key="manga.title"
        class="border-2 border-gray-300 rounded-lg shadow-xl bg-white overflow-hidden flex flex-col mb-8"
        style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);"
      >
        <!-- Manga Card -->
        <div class="relative">
          <!-- Favorite Button -->
          <button 
            @click.prevent="toggleFavorite(manga)"
            class="absolute top-2 right-2 bg-white rounded-full p-2 shadow hover:bg-gray-100 z-10"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="isFavorite(manga) ? 'text-red-500' : 'text-gray-400'" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>

          <router-link :to="{ name: 'mangaDetail', params: { mangaId: getMangaID(manga.latestChapter) } }">
            <!-- Image -->
            <div class="h-64 w-full" style="min-height: 250px;">
              <img
                :src="getImageSrc(manga.img_path)"
                alt="Manga cover"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- Text content -->
            <div class="p-6 bg-white flex-1 flex flex-col justify-between">
              <div>
                <!-- Title -->
                <h2 class="text-xl font-bold mb-3 min-h-[48px] line-clamp-2">
                  {{ manga.title }}
                </h2>
                
                <!-- Chapter and views -->
                <div class="flex items-center justify-center mb-3 min-h-[32px]">
                  <div class="mr-4">
                    <span class="text-sm font-medium text-gray-500">Latest Chapter:</span>
                    <span class="text-sm">{{ getChapterID(manga.latestChapter) }}</span>
                  </div>
                  <div>
                    <span class="text-sm font-medium text-gray-500">Views:</span>
                    <span class="text-sm">{{ manga.views }}</span>
                  </div>
                </div>

                <!-- Description -->
                <p class="text-sm text-gray-600 mb-3 min-h-[60px] line-clamp-3">
                  {{ truncateDescription(manga.description) }}
                </p>

                <!-- Genres container -->
                <div class="flex flex-wrap gap-2 mb-3 flex-grow-0" ref="genresContainer">
                  <template v-for="(genre, index) in manga.genres" :key="index">
                    <span 
                      class="px-2 py-1 text-xs rounded cursor-pointer transition-colors" 
                      :class="genre === selectedGenre ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'"
                      @click.prevent="selectedGenre = genre"
                    >
                      {{ genre }}
                    </span>
                  </template>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
    
    <!-- No results message -->
    <div v-if="filteredMangaList.length === 0" class="text-center py-12">
      <div class="text-gray-500 text-lg">No manga found matching your filters</div>
      <button 
        @click="resetFilters" 
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        Reset Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';

const mangaList = ref([]);
const searchQuery = ref('');
const selectedGenre = ref('');
const sortBy = ref('title');
const favorites = ref([]);

// Load favorites from localStorage
const loadFavorites = () => {
  const storedFavorites = localStorage.getItem('mangaFavorites');
  if (storedFavorites) {
    favorites.value = JSON.parse(storedFavorites);
  }
};

// Save favorites to localStorage
const saveFavorites = () => {
  localStorage.setItem('mangaFavorites', JSON.stringify(favorites.value));
};

// Toggle favorite status
const toggleFavorite = (manga) => {
  const mangaId = getMangaID(manga.latestChapter);
  const index = favorites.value.findIndex(id => id === mangaId);
  
  if (index === -1) {
    favorites.value.push(mangaId);
  } else {
    favorites.value.splice(index, 1);
  }
  
  saveFavorites();
};

// Check if manga is favorite
const isFavorite = (manga) => {
  const mangaId = getMangaID(manga.latestChapter);
  return favorites.value.includes(mangaId);
};

// Get all unique genres across all manga
const allGenres = computed(() => {
  const genres = new Set();
  mangaList.value.forEach(manga => {
    if (manga.genres && Array.isArray(manga.genres)) {
      manga.genres.forEach(genre => genres.add(genre));
    }
  });
  return Array.from(genres).sort();
});

// Filter and sort manga list
const filteredMangaList = computed(() => {
  let filtered = [...mangaList.value];
  
  // Filter by search query
  if (searchQuery.value.trim() !== '') {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(manga => 
      manga.title.toLowerCase().includes(query) || 
      manga.description.toLowerCase().includes(query)
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

// Reset all filters
const resetFilters = () => {
  searchQuery.value = '';
  selectedGenre.value = '';
  sortBy.value = 'title';
};

const getChapterID = (chapterPath) => {
  const parts = chapterPath.split('\\');
  return parts[parts.length - 1];
};

const getMangaID = (chapterPath) => {
  const parts = chapterPath.split('\\');
  return parts[parts.length - 2];
};

const getImageSrc = (imgPath) => {
  return imgPath || '/api/placeholder/400/640';
};

const truncateDescription = (desc) => {
  if (!desc) return '';
  const cleanDesc = desc.replace(/You are reading.*?bookmark\.\n\n\s+/s, '');
  if (cleanDesc.length > 200) {
    return cleanDesc.substring(0, 200) + '...';
  }
  return cleanDesc;
};

onMounted(async () => {
  loadFavorites();
  
  try {
    const response = await fetch('/manga_store/store.json');
    if (response.ok) {
      mangaList.value = await response.json();
    } else {
      console.error('Failed to load manga list:', response.statusText);
    }
  } catch (error) {
    console.error('Error loading manga list:', error);
  }
});
</script>