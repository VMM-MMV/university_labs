<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">My Favorites</h1>
    
    <!-- Empty state -->
    <div v-if="favoriteMangaList.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <div class="text-gray-500 text-lg mb-4">You haven't added any manga to your favorites yet</div>
      <router-link to="/" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
        Browse Manga
      </router-link>
    </div>
    
    <!-- Manga Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
      <div
        v-for="manga in favoriteMangaList"
        :key="manga.title"
        class="border-2 border-gray-300 rounded-lg shadow-xl bg-white overflow-hidden flex flex-col mb-8"
        style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);"
      >
        <!-- Manga Card -->
        <div class="relative">
          <!-- Remove from Favorites Button -->
          <button 
            @click="removeFromFavorites(manga)"
            class="absolute top-2 right-2 bg-white rounded-full p-2 shadow hover:bg-gray-100 z-10"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
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
                <div class="flex flex-wrap gap-2 mb-3 flex-grow-0">
                  <template v-for="(genre, index) in manga.genres" :key="index">
                    <span class="px-2 py-1 text-xs rounded bg-gray-200">
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const mangaList = ref([]);
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

// Remove manga from favorites
const removeFromFavorites = (manga) => {
  const mangaId = getMangaID(manga.latestChapter);
  const index = favorites.value.findIndex(id => id === mangaId);
  
  if (index !== -1) {
    favorites.value.splice(index, 1);
    saveFavorites();
  }
};

// Filter manga list to only show favorites
const favoriteMangaList = computed(() => {
  return mangaList.value.filter(manga => {
    const mangaId = getMangaID(manga.latestChapter);
    return favorites.value.includes(mangaId);
  });
});

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